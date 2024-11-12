# %%
# Import Libraries
# import requests
# from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Initialize data storage
data = [] 


# Function to format state to abbreviations
def format_state(state_name):
    state_abbr = {
        "California": "CA",
        "Colorado": "CO",
        # Add other state as needed
    }
    return state_abbr.get(state_name, state_name)  # Default to state_name if not found

    # Function to Close Google Ads
def close_google_ad():
    if "#google_vignette" in driver.current_url:
        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "close_button"))
            )
            close_button.click()
            logging.info("Closed Google ad")
        except NoSuchElementException:
           logging.warning("Google ad pop-up not found")


# Data extraction function
def extract_data_from_page(url, data):
    logging.info(f"Extracting data from: {url}")
    driver.get(url)
    
    # Close Google ad if present
    close_google_ad
    
    # Wait for the "centercolumndepartment" div to load
    try:
        center_column = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "centercolumndepartment"))
        )
    except:
        logging.warning("centercolumndepartment not found after waiting")
        return  # Exit function if the element is not found
    
    # Extract department name
    try:
        department_name_element = center_column.find_element(By.TAG_NAME, "h1")
        department_name = department_name_element.text.strip()
    except NoSuchElementException:
        department_name = ""
    print("Department Name:", department_name)  # Debug print

    # Extract title
    try:
        title_element = driver.find_element(By.CLASS_NAME, "title")
        title = title_element.text.strip()
    except NoSuchElementException:
        title = ""
    print("Title:", title)  # Debug print

    # Extract the information from the "departmentinfo" div
    try:
        department_info_element = driver.find_element(By.CLASS_NAME, "departmentinfo")
        info_text = department_info_element.get_attribute("innerHTML").split("<br>")
        info_text = [line.strip() for line in info_text if line.strip()]  # Remove empty lines and strip whitespace

        # Extract first and last name
        name_parts = info_text[0].split()
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        #*******CONTINUE 
        # Optional: Extract building name if present
        building_name = info_text[1] if "Headquarters" in info_text[1] else ""
        address_index = 2 if building_name else 1  # Adjust index based on presence of building name
        address = info_text[address_index]

        # Extract city, state, and zip code from the next line
        city_state_zip = info_text[address_index + 1]
        city, state_zip = city_state_zip.split(", ")
        state, zip_code = state_zip.split() if " " in state_zip else (state_zip, "")

        # Extract phone number using a regular expression
        phone_line = next((line for line in info_text if "Phone:" in line), "")
        phone_number = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_line)
        phone = phone_number.group() if phone_number else ""

        # Extract county from the line containing "County:" and an anchor tag
        county_line = next((line for line in info_text if "County:" in line), "")
        county = re.search(r'County:.*?>(.*?)<', county_line)
        county = county.group(1) if county else ""

    except NoSuchElementException:
        first_name = last_name = building_name = address = city = state = zip_code = phone = county = ""

    # Debug prints to verify extracted data
    print("First Name:", first_name)
    print("Last Name:", last_name)
    print("Building Name:", building_name)
    print("Address:", address)
    print("City:", city)
    print("State:", state)
    print("ZIP Code:", zip_code)
    print("Phone:", phone)
    print("County:", county)

    # Append extracted data to the list
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
        "phone": phone,
        "county": county  # Add county to the data dictionary
    })





# %%
# Main Extraction Process

# Define base URL
base_url = "https://www.usacops.com/co/shrflist.html"


# %%
# Save Data to CSV
df = pd.DataFrame(data, columns=[
    "department_name", "title", "first_name", "last_name", 
    "building_name", "address", "city", "state", "zip_code", "phone", "county"
])

output_path = r"C:\Users\jchan\csi360_fire_police\co_lefd_contact_num\resources\output\extracted_data.csv"
df.to_csv(output_path, index=False)
logging.info(f"Data successfully saved to {output_path}")

# Quit the WebDriver
driver.quit()

# %%



