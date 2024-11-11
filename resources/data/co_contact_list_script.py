# %%
# Import Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin  # For handling relative URLs
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging for debug purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configure the Chrome WebDriver options for headless execution if preferred
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Comment this line to see browser actions

# Start the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Initialize 'data' as an empty list
data = []  # This needs to be defined before it's used in data.append(...)


# %%
# Helper Functions for Data Extraction

# Function to format state to abbreviations
def format_state(state_name):
    # Dictionary of state abbreviations
    state_abbr = {
        "California": "CA",
        "Colorado": "CO",
        # Add other state mappings as needed
    }
    return state_abbr.get(state_name, state_name)  # Default to state_name if not found

def format_phone(phone):
    phone_digits = re.sub(r"\D", "", phone)  # Remove non-digit characters
    return f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:10]}" if len(phone_digits) >= 10 else phone

def safe_extract_text(soup, selector, default=""):
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else default


# Data extraction function
def extract_data_from_page(url, data):
    logging.info(f"Extracting data from: {url}")
    driver.get(url)

    # Function to Close Google Ads
    if "#google_vignette" in driver.current_url:
        try:
            driver.find_element(By.ID, "close_button").click()
        except NoSuchElementException:
            logging.warning("Google ad pop-up not found")

# %%
# Parse page content
soup = BeautifulSoup(driver.page_source, "html.parser") #remove to better target nested element departmentname
center_column = soup.find("div", class_="centercolumndepartment") # Insert to provide better targeting of departmentname
department_name = safe_extract_text(soup, "h1.departmentname")
title = safe_extract_text(soup, "div.title")
print("Department Name:", department_name)  # Debug print

logging.info(f"Department Name: {department_name}, Title: {title}")


# Extract department information
department_info = soup.find("div", class_="departmentinfo")
info_lines = department_info.get_text(separator="\n").splitlines() if department_info else []
    
first_name = info_lines[0].split()[0] if info_lines and len(info_lines[0].split()) > 0 else ""
last_name = info_lines[0].split()[1] if info_lines and len(info_lines[0].split()) > 1 else ""
building_name = info_lines[1] if len(info_lines) > 1 else ""
address = info_lines[2] if len(info_lines) > 2 else ""
    
city_state_zip = info_lines[3] if len(info_lines) > 3 else ""
city = city_state_zip.split(",")[0] if "," in city_state_zip else ""
state = format_state(city_state_zip.split(",")[1].strip().split()[0]) if "," in city_state_zip else ""
zip_code = city_state_zip.split()[-1] if len(city_state_zip.split()) > 1 else ""
    
# County extraction
county = safe_extract_text(department_info, "a") if department_info else ""

# Append the extracted data
data.append({
    "department_name": department_name,
    "title": title,
    "first_name": first_name,
    "last_name": last_name,
    "building_name": building_name,
    "address": address,
    "city": city,
    "state": state,
    "zip_code": zip_code,
    "county": county
})
logging.info(f"Data extracted for {department_name}")

# %%
# Main Extraction Process

# Define base URL
base_url = "https://www.usacops.com/co/shrflist.html"

# Load the main page
driver.get(base_url)
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find both divs with the class "centercolumnnested2all links within main page"
link_divs = soup.find_all("div", class_="centercolumnnested2")

# Loop through each div and collect links
for link_div in link_divs:
    links = link_div.find_all("a", href=True)
    for link in links:
        target_url = urljoin(base_url, link["href"])
        extract_data_from_page(target_url, data)

        # Delay adjust between requests to prevent timeout
        time.sleep(3) # Adjust as needed for server load

print(soup.prettify())  # View the full HTML structure for debugging


print("Extracted data:", {
    "department_name": department_name,
    "title": title,
    "first_name": first_name,
    "last_name": last_name,
    "building_name": building_name,
    "address": address,
    "city": city,
    "state": state,
    "zip_code": zip_code,
    "county": county
})

# %%
# Save Data to CSV
df = pd.DataFrame(data, columns=[
    "department_name", "title", "first_name", "last_name", 
    "building_name", "address", "city", "state", "zip_code", "county"
])

output_path = r"C:\Users\jchan\csi360_fire_police\co_lefd_contact_num\resources\output\extracted_data.csv"
df.to_csv(output_path, index=False)
logging.info(f"Data successfully saved to {output_path}")

# Quit the WebDriver
driver.quit()

# %%



