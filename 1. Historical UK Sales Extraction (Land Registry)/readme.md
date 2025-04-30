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

Install all dependencies using `pip`:

```bash
pip install selenium pandas webdriver-manager
