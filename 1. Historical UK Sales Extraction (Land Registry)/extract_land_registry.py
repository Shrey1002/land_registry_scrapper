from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import tkinter as tk
from tkinter import filedialog


import pandas as pd

# Create a list to hold all transactions
all_transactions = []

# List of postal codes to query
postal_codes = [
    'SW1',  # Belgravia, Pimlico, Westminster
    'SW3',  # Chelsea
    'SW7',  # South Kensington, Knightsbridge
    'W1',   # Mayfair, Marylebone, Soho
    'W8',   # Kensington
    'NW1',  # Regent's Park, Primrose Hill
    'WC1',  # Bloomsbury, Holborn
    'WC2',  # Covent Garden, Strand
    'EC1',  # Clerkenwell, Finsbury
    'EC2',  # Moorgate, Liverpool Street
    'EC3',  # Aldgate, Fenchurch Street
    'EC4'   # St. Paul's, Fleet Street
]


#  Prompt user for dates using tkinter 
def get_date_range():
    date_values = {'from': None, 'to': None}
    def submit():
        date_values['from'] = from_entry.get()
        date_values['to'] = to_entry.get()
        root.destroy()

    root = tk.Tk()
    root.title("Enter Date Range")
    tk.Label(root, text="Start Date (MM/DD/YYYY):").grid(row=0, column=0, padx=10, pady=5)
    from_entry = tk.Entry(root)
    from_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="End Date (MM/DD/YYYY):").grid(row=1, column=0, padx=10, pady=5)
    to_entry = tk.Entry(root)
    to_entry.grid(row=1, column=1, padx=10, pady=5)

    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

    return date_values['from'], date_values['to']

# Fetch dates from user
date_from, date_to = get_date_range()


#  Setup Chrome options 
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

#  Launch WebDriver 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://landregistry.data.gov.uk/app/ppd/")

wait = WebDriverWait(driver, 20)

# Main loop through each postcode
for postal_code in postal_codes:
    try:
        # Wait and input the postal code
        postcode_input = wait.until(EC.presence_of_element_located((By.ID, 'postcode')))
        postcode_input.clear()
        postcode_input.send_keys(postal_code)
        
        # Input date range
        from_input = driver.find_element(By.NAME, 'min_date')
        from_input.clear()
        from_input.send_keys(date_from)

        to_input = driver.find_element(By.NAME, 'max_date')
        to_input.clear()
        to_input.send_keys(date_to)
        # Select the 'All' radio button
        all_radio = driver.find_element(By.CSS_SELECTOR, 'input[name="limit"][value="all"]')
        all_radio.click()


        # Click Search button
        search_button = driver.find_element(By.XPATH, "//button[@type='submit']" )
        search_button.click()

        # Wait for results (this part might need adjustment based on the site's behavior)
        time.sleep(5)

        try:
            no_results_text = driver.find_element(By.XPATH, "//p[contains(text(), 'Found 0 transactions')]")
            if no_results_text.is_displayed():
                print(f"No transactions found for postal code: {postal_code}")
                driver.get("https://landregistry.data.gov.uk/app/ppd/")
                time.sleep(2)
                continue
        except:
            print(f"Transactions found for postal code: {postal_code}")

            # Wait for the download link to be clickable
            # Find the <i> icon first
            download_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//i[contains(@class, 'fa-download')]")))

            # Go up to the parent <a> tag
            download_data_button = download_icon.find_element(By.XPATH, "./parent::a")

            # Scroll into view and click via JavaScript
            driver.execute_script("arguments[0].scrollIntoView(true);", download_data_button)
            driver.execute_script("arguments[0].click();", download_data_button)

            print(f"Clicked 'Download data' button for postal code: {postal_code}")


            time.sleep(2)

            # Step 2: Click the 'Get all results as CSV' button
            csv_download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@class='no-border']//a[contains(@href, '.csv')]")))
            
            csv_url = csv_download_button.get_attribute('href')
            print(f"CSV URL fetched: {csv_url}")

            # Step 2: Fetch the CSV data directly
            df = pd.read_csv(csv_url, header=None)
            all_transactions.append(df)

            # Step 3: Save locally
            print(f"Clicked 'Get all results as CSV' button for postal code: {postal_code}")

            time.sleep(5)
            
            # Step 3: After download, go back to starting page for next postal code
            driver.get("https://landregistry.data.gov.uk/app/ppd/")
            time.sleep(2)
            continue


    except Exception as e:
        print(f"Error processing postal code {postal_code}: {e}")


if all_transactions:
    final_df = pd.concat(all_transactions, axis=0, ignore_index=True)

    final_df = final_df[[1, 2, 3]]
    final_df.columns = ['Selling Price', 'Transaction Date', 'Postcode']
    # Save merged DataFrame to one CSV
    final_df.to_csv("land_registry_sales.csv", index=False)
    print("Successfully saved merged data into 'land_registry_sales.csv'")
else:
    print("No data found for any postal code.")
#  Close the browser 
driver.quit()