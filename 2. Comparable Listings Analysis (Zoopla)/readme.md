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
git clone https://github.com/your-username/zoopla-postcode-scraper.git
cd zoopla-postcode-scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```
