import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import logging
import traceback
from fuzzywuzzy import fuzz
import string

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

state_abbreviations = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
    'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

def get_address_details(driver, institution_name):
    institution_name_text = ""
    city = ""
    website = ""
    phone_number = ""

    try:
        # Open Google Maps
        driver.get("https://www.google.com/maps")
        time.sleep(3)  # Wait for the page to load

        # Find the search box and enter the institution name
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(institution_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for the search results to load

        try:
            # Get the institution name from the result page
            institution_element = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf.lfPIob")
            institution_name_text = institution_element.text

            # Try to click the "Copy address" button
            copy_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Copy address']")
            copy_button.click()
            time.sleep(1)  # Wait for the address to be copied to the clipboard

        except Exception:
            # If the "Copy address" button is not found, click the first search result
            try:
                first_result = driver.find_element(By.CSS_SELECTOR, "a[aria-label]")
                first_result.click()
                time.sleep(3)  # Wait for the new page to load

                # Get the institution name from the new page
                institution_element = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf.lfPIob")
                institution_name_text = institution_element.text

                # Try to click the "Copy address" button again
                copy_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Copy address']")
                copy_button.click()
                time.sleep(1)  # Wait for the address to be copied to the clipboard

            except Exception as e:
                logging.error(f"Copy address button not found for {institution_name}: {e}")
                return institution_name_text, city, website, phone_number

        # Get the address from the clipboard
        address = pyperclip.paste()
        city = extract_city_from_address(address)

        # Extract website and phone number using copy buttons
        try:
            website_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Copy website']")
            website_button.click()
            time.sleep(1)
            website = pyperclip.paste()
        except Exception as e:
            try:
                website_button = driver.find_element(By.CSS_SELECTOR, "button[data-tooltip='Copy website']")
                website_button.click()
                time.sleep(1)
                website = pyperclip.paste()
            except Exception as e:
                logging.error(f"Copy website button not found for {institution_name}: {e}")

        try:
            phone_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Copy phone number']")
            phone_button.click()
            time.sleep(1)
            phone_number = pyperclip.paste()
        except Exception as e:
            try:
                phone_button = driver.find_element(By.CSS_SELECTOR, "button[data-tooltip='Copy phone number']")
                phone_button.click()
                time.sleep(1)
                phone_number = pyperclip.paste()
            except Exception as e:
                logging.error(f"Copy phone number button not found for {institution_name}: {e}")

    except Exception as e:
        logging.error(f"Error occurred: {e}")

    return institution_name_text, city, website, phone_number

def extract_city_from_address(address):
    # Split the address by commas
    parts = address.split(',')
    # The city should be the second part
    if len(parts) > 1:
        city = parts[1].strip()
        return city
    return ""

def initialize_driver(driver_path):
    try:
        service = Service(driver_path)
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)
        logging.info("Initialized Edge WebDriver.")
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize Edge WebDriver: {e}")
        return None

def verify_addresses(input_csv, output_csv, start_index=0):
    # Read the CSV file
    df = pd.read_csv(input_csv)
    logging.info(f"Loaded input CSV file with {len(df)} rows.")

    # Add new columns for city, website, and phone number
    if 'city' not in df.columns:
        df['city'] = ''
    if 'website' not in df.columns:
        df['website'] = ''
    if 'phone_number' not in df.columns:
        df['phone_number'] = ''

    # Path to the Edge WebDriver executable
    driver_path = "C:/Users/klin/OneDrive - PTC/msedgedriver.exe"
    driver = initialize_driver(driver_path)
    if not driver:
        logging.error("Failed to initialize WebDriver. Exiting.")
        return

    try:
        # Iterate through the rows starting from start_index
        for index in range(start_index, len(df)):
            row = df.iloc[index]
            search_string = f"{row['instnm']} {row['state']}".strip()
            logging.info(f"Processing row {index}: {search_string}")

            try:
                institution_name_text, city, website, phone_number = get_address_details(driver, search_string)

                # Remove punctuation from the strings for matching
                cleaned_name = remove_punctuation(row['instnm'].strip().lower())
                cleaned_institution_name = remove_punctuation(institution_name_text.strip().lower())
                cleaned_verified_address = remove_punctuation(city.lower())

                # Perform fuzzy matching
                name_match = fuzz.partial_ratio(cleaned_name, cleaned_institution_name)
                logging.info(f"Fuzzy match score for row {index}: {name_match}")

                state_full_name = row['state'].strip()
                state_abbr = state_abbreviations.get(state_full_name, '').lower()
                state_match = state_abbr in cleaned_verified_address
                logging.info(f"State match for row {index}: {state_match}")

                if name_match > 90 and state_match:
                    # Update the DataFrame with the extracted details
                    df.at[index, 'city'] = city
                    df.at[index, 'website'] = website
                    df.at[index, 'phone_number'] = phone_number
                else:
                    df.at[index, 'city'] = ''
                    df.at[index, 'website'] = ''
                    df.at[index, 'phone_number'] = ''

                # Save progress to the output CSV file after each row
                df.to_csv(output_csv, index=False)
                logging.info(f"Processed row {index} and updated CSV.")

            except Exception as e:
                logging.error(f"Error processing row {index}: {e}")
                traceback.print_exc()

    finally:
        # Close the browser
        driver.quit()
        logging.info("Closed Edge WebDriver.")

    logging.info(f"Verification completed. Results saved to {output_csv}")

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

# Example usage
verify_addresses('all_us_colleges.csv', 'verified_collegesend.csv', start_index=5517)
