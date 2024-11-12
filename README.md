# Colorado Law Enforcement and Fire Department Scraper for CSI360

<p align="center">
<img src="images/CSI360-Logo-2022.png" width="720">
</p>

## Description
This Python-based web scraping application is designed to support CSI360's inside sales campaign by gathering contact information for law enforcement and fire departments in Colorado. Targeted data includes department names, locations, contact details, and county information, which is intended to help sales representatives leverage CSI360’s existing customer base as references to attract new clients. This project highlights data extraction, web automation, and data processing capabilities within a practical business context.

## Table of Contents
- [Description](#description)
- [Tools and Libraries Used](#tools-and-libraries-used)
- [Setup and Usage](#setup-and-usage)
- [Data Collection Process](#data-collection-process)


## Tools and Libraries
This project relies on the following tools for data extraction and processing:
- **Selenium WebDriver**: Automates web browser interaction to gather data.
- **Pandas**: Manages and exports data in structured formats (CSV).
- **Regular Expressions (re)**: Parses and formats phone numbers and addresses.
- **Logging**: Tracks scraping progress and helps debug issues.
- **Jupyter Notebook**: Primary environment for developing and running the script.
- **Visual Studio Code**: Used for debugging and testing.


## Setup and Usage
To set up the environment, use the following commands to install necessary libraries:
```bash
conda install -c anaconda selenium
conda install -c conda-forge webdriver-manager
```
   - **Configure Chrome WebDriver**: The script uses `webdriver-manager` to automatically handle ChromeDriver. Make sure Google Chrome is installed on your machine.

## Data Collection Process
This application uses Selenium WebDriver to automate browsing and data extraction from a target website listing Colorado law enforcement and fire department contacts.

1. **Web Navigation**: The script initializes a Chrome WebDriver, navigates to the target page, and closes any pop-up ads, ensuring uninterrupted access to data.

2. **Iterative Page Looping**: The script identifies and iterates through multiple `div` elements containing contact links. For each contact link, it opens a new page to extract the relevant contact information before returning to the main page to continue the loop. This approach ensures that data from all available pages is gathered.

3. **Data Extraction**: For each agency page, key details such as department name, title, address, phone number, and county are extracted. State names are abbreviated, phone numbers are formatted, and missing or optional fields are handled gracefully.

4. **Data Storage**: All extracted data is stored in a Pandas DataFrame and saved as a CSV file for CSI360’s sales team to use in identifying and contacting potential clients in the Colorado area.

This structured, automated process streamlines the data-gathering workflow, ensuring the sales team has a reliable, organized dataset for their campaign.
