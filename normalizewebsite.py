import pandas as pd
import re

def normalize_website(url):
    if pd.isna(url) or url.strip() == '':
        return ''
    
    # Ensure the input is a string
    url = str(url)
    
    # Remove http:// or https://
    url = re.sub(r'http(s)?://', '', url)
    
    # Ensure the URL starts with www.
    if not url.startswith('www.'):
        url = 'www.' + url
    
    # Remove trailing slashes
    url = url.rstrip('/')
    
    # Convert to lowercase
    url = url.lower()
    
    # Remove anything after the domain extension
    url = re.sub(r'(\.com|\.edu|\.net|\.org|\.gov|\.co|\.uk)([/?].*)?$', r'\1', url)
    
    return url

def normalize_phone_number(phone):
    phone = str(phone)
    if pd.isna(phone) or phone.strip() == '':
        return ''
    
    # Remove all non-numeric characters except for the plus sign
    phone = re.sub(r'[^\d]', '', phone)
    
    # Check if the phone number starts with '1' and has 11 digits
    if phone.startswith('1') and len(phone) == 11:
        # Remove the '1' and format to the standard US format
        phone = phone[1:]
        return f'({phone[:3]}) {phone[3:6]}-{phone[6:]}'
    
    return phone  # Return as-is if it does not match the expected format

def normalize_fields(csv_file, output_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Normalize the website field
    if 'website' in df.columns:
        df['website'] = df['website'].apply(normalize_website)
    else:
        print("No 'website' column found in the CSV file.")
    
    # Normalize the phone_number field
    if 'phone_number' in df.columns:
        df['phone_number'] = df['phone_number'].apply(normalize_phone_number)
    else:
        print("No 'phone_number' column found in the CSV file.")
    
    # Save the updated dataframe to a new CSV file
    df.to_csv(output_file, index=False)
    print(f'Normalized websites and phone numbers saved to {output_file}')

# Example usage
input_csv = 'rough_complete_college_list.csv'  # Replace with your input CSV file
output_csv = 'output_normalized.csv'  # Replace with your desired output CSV file
normalize_fields(input_csv, output_csv)
