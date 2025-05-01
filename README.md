# 🏠 Land Registry Sales Data Scraper

This Python project allows you to automate downloading **property sales data** from the UK Land Registry portal for specific postal codes and a date range using **Selenium and Tkinter**. The script navigates the site, inputs the criteria, downloads CSV files, and consolidates the results into a single CSV file: `land_registry_sales.csv`.

---

## 🚀 Features

- Search by multiple **London postal districts**
- Interactive **GUI date selector** for date range input
- **Automated browser navigation** using Selenium
- Skips postcodes with no results
- Downloads and combines all results into one CSV file
- Clean logs and error handling

---

## 📦 Dependencies

Install all dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Script
To execute the program, run the following command in your terminal:

```bash
python extract_land_registry.py
```

# 🏘️ Zoopla Property Listing Scraper (Postcode-Based)

This Python script automates the retrieval of residential property listings from the Zoopla platform using:

- 📦 The **Zoopla API (via RapidAPI)** for property metadata  
- 🧭 **Selenium automation** for scraping square footage (`sq ft` or `sq m`)  
- 📂 A user-selected CSV input containing postcodes  
- 📝 Final data exported to a single CSV file: `zoopla_listings.csv`

---

## ✅ Features

- Reads postcodes from a CSV file (via file picker)
- Fetches property listing data for each postcode using the Zoopla API
- Extracts:
  - Listing ID
  - Property address
  - Sales agent name
  - Asking price
  - Area (sq ft or sq m), if available
- Skips any listing that triggers a Cloudflare CAPTCHA page
- Merges all data into one CSV report

---

## 🛠 Requirements

- Python 3.8+
- Google Chrome (must be installed)
- A free API key from [Zoopla's RapidAPI page](https://rapidapi.com/apidojo/api/zoopla)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Shrey1002/land_registry_scrapper.git
cd 2. Comparable Listings Analysis (Zoopla)
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Script
```bash
python scrape_zoopla.py
```


