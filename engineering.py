import pandas as pd
import re
from fuzzywuzzy import fuzz

# Read the first CSV file
df1 = pd.read_csv('updated_csv_file.csv')

# Read the second CSV file
df2 = pd.read_csv('engineering_universities.csv')

# Function to clean state fields
def clean_state(state):
    return re.sub(r'[^a-zA-Z]', '', state)

# Clean the 'Billing State' column in df1
df1['Billing State'] = df1['Billing State'].apply(clean_state)

# Clean the 'State' column in df2
df2['State'] = df2['State'].apply(clean_state)

# Create a dictionary from df2 for efficient lookup
city_state_to_institutions = {}
for index, row in df2.iterrows():
    key = (row['City'], row['State'])
    if key not in city_state_to_institutions:
        city_state_to_institutions[key] = []
    city_state_to_institutions[key].append(row['Name of Institution'])

# Function to perform lenient matching
def is_engineering_university(instnm, billing_city, billing_state, lookup_dict):
    institutions = lookup_dict.get((billing_city, billing_state), [])
    for institution in institutions:
        if fuzz.partial_ratio(instnm, institution) >= 75:  # Using partial_ratio for more lenient matching
            return True
    return False

# Apply the matching function to create the 'Engineering University' column
df1['Engineering University'] = df1.apply(
    lambda row: is_engineering_university(row['instnm'], row['city'], row['Billing State'], city_state_to_institutions), axis=1
)

# Save the updated DataFrame back to a CSV file
df1.to_csv('updated_first_csv_file.csv', index=False)
