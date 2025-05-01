import requests
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import filedialog

#  Function to extract area from a listing page 
def get_area_from_listing(listing_id):
    url = f"https://www.zoopla.co.uk/for-sale/details/{listing_id}"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    def extract_sqft_from_text(text):
        match = re.search(r"\b[\d,]+ ?sq\.? ?ft\b", text, re.I)
        return match.group() if match else None

    try:
        driver.get(url)

        #  Detect CAPTCHA 
        time.sleep(2)  # Allow time for redirect to Cloudflare if it's happening
        if "cloudflare" in driver.title.lower() or "attention required" in driver.title.lower():
            print(f"⚠️ CAPTCHA detected for listing ID {listing_id}. Skipping...")
            return "Skipped (CAPTCHA)"

        # Accept cookies
        try:
            accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "accept")))
            accept_btn.click()
        except:
            pass

        # Look for area in bullet features
        try:
            key_features = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li._1wmbmfq2 p")))
            for feature in key_features:
                text = feature.text.strip()
                area = extract_sqft_from_text(text)
                if area:
                    return area
        except:
            pass

        # Fallback: description
        try:
            try:
                read_more_btn = wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(., 'Read full description')]"
                )))
                read_more_btn.click()
                time.sleep(1)
            except:
                pass

            full_description = wait.until(EC.presence_of_element_located((By.ID, "detailed-desc"))).text
            area = extract_sqft_from_text(full_description)
            return area if area else "N/A"
        except:
            return "N/A"

    finally:
        driver.quit()

# Function to fetch listings from Zoopla API 
def fetch_listings_for_postcode(postcode):
    url = "https://zoopla.p.rapidapi.com/properties/v2/list"
    headers = {
        "x-rapidapi-key": "2d467f0d1fmsh24a48c03413165bp1a261ajsn1265b431cbe6",
        "x-rapidapi-host": "zoopla.p.rapidapi.com"
    }
    params = {
        "locationValue": postcode,
        "category": "residential",
        "furnishedState": "Any",
        "sortOrder": "newest_listings",
        "page": "1"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}")
        return []

    listings_data = response.json().get("data", {}).get("listings", {})

    # Try extended first, then fall back to regular if extended is None
    listings = listings_data.get("regular")
    if listings is None:
        print("regular listings not available, falling back to regular listings.")
        listings = listings_data.get("extended", [])

    return listings

# Initialize Tkinter root and hide the main window
root = tk.Tk()
root.withdraw()

# Open a file dialog to select the CSV file
csv_file = filedialog.askopenfilename(
    title="Select CSV File with Postcodes",
    filetypes=[("CSV Files", "*.csv")]
)

# Exit if no file is selected
if not csv_file:
    print("No file selected. Exiting.")
    exit()


df = pd.read_csv(csv_file)

# Drop missing values and get list of postcodes
postcodes = df['Postcode'].dropna().unique().tolist()

all_data = []


#  Main loop 
for postcode in postcodes:
    print(f"\n Fetching listings for: {postcode} ")
    listings = fetch_listings_for_postcode(postcode)
    for listing in listings:
        address = listing.get("address", "N/A")
        agent = listing.get("agent", {}).get("branchName", "N/A")
        price = listing.get("pricing", {}).get("label", "N/A")
        listing_id = listing.get("listingId", "N/A")

        print("\n Listing ")
        print(f"ID: {listing_id}")
        print(f"Address: {address}")
        print(f"Agent: {agent}")
        print(f"Price: {price}")

        # Now fetch area in sq. ft
        area = get_area_from_listing(listing_id)
        print(f"Area: {area}")
        print("-" * 40)

                # Save row
        all_data.append({
            "ZooplaListingId": listing_id,
            "House Address": address,
            "Sales Agent Name": agent,
            "Asking Price": price,
            "Area (sq ft or sq m)": area
        })

#  Save to CSV 
output_df = pd.DataFrame(all_data)
output_df.to_csv("zoopla_listings.csv", index=False)
print("\n✅ Data saved to 'zoopla_listings.csv'")