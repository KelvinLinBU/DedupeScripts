import pandas as pd

# Create a mapping from state abbreviations to state names
state_abbreviation_to_name = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
}

# Sample dictionary for location to owner mapping
owner1 = "Nick Cross"
owner2 = "Jess Barbara"
location_to_owner_USCanada = {
    ('Alabama', 'United States'): owner2,
    ('Arizona', 'United States'): owner2,
    ('Arkansas', 'United States'): owner2,
    ('California', 'United States'): owner2,
    ('Colorado', 'United States'): owner2,
    ('Delaware', 'United States'): owner2,
    ('Florida', 'United States'): owner2,
    ('Georgia', 'United States'): owner2,
    ('Kansas', 'United States'): owner2,
    ('Kentucky', 'United States'): owner2,
    ('Louisiana', 'United States'): owner2,
    ('Maryland', 'United States'): owner2,
    ('Mississippi', 'United States'): owner2,
    ('Nevada', 'United States'): owner2,
    ('Missouri', 'United States'): owner2,
    ('New Mexico', 'United States'): owner2,
    ('North Carolina', 'United States'): owner2,
    ('Oklahoma', 'United States'): owner2,
    ('South Carolina', 'United States'): owner2,
    ('Tennessee', 'United States'): owner2,
    ('Texas', 'United States'): owner2,
    ('Utah', 'United States'): owner2,
    ('Virginia', 'United States'): owner2,
    ('District of Columbia', 'United States'): owner2,
    ('West Virginia', 'United States'): owner2,
    ('Alaska', 'United States'): owner2,
    ('Hawaii', 'United States'): owner2,
    ('', 'Canada'): owner2,
    ('Idaho', 'United States'): owner1,
    ('Illinois', 'United States'): owner1,
    ('Indiana', 'United States'): owner1,
    ('Iowa', 'United States'): owner1,
    ('Maine', 'United States'): owner1,
    ('Massachusetts', 'United States'): owner1,
    ('Michigan', 'United States'): owner1,
    ('Minnesota', 'United States'): owner1,
    ('Montana', 'United States'): owner1,
    ('Nebraska', 'United States'): owner1,
    ('New Hampshire', 'United States'): owner1,
    ('New Jersey', 'United States'): owner1,
    ('New York', 'United States'): owner1,
    ('North Dakota', 'United States'): owner1,
    ('Ohio', 'United States'): owner1,
    ('Oregon', 'United States'): owner1,
    ('Pennsylvania', 'United States'): owner1,
    ('Rhode Island', 'United States'): owner1,
    ('South Dakota', 'United States'): owner1,
    ('Vermont', 'United States'): owner1,
    ('Washington', 'United States'): owner1,
    ('Wisconsin', 'United States'): owner1,
    ('Wyoming', 'United States'): owner1,
}

# Read the CSV file into a DataFrame
df = pd.read_csv('normalized_and_filled2.csv')

# Map the state abbreviations to full state names
df['State Name'] = df['Billing State'].map(state_abbreviation_to_name)

# Assign owners based on the full state names
def assign_owner(row):
    state_name = row['State Name']
    country = 'United States'  # Assuming the country is the United States for this example
    return location_to_owner_USCanada.get((state_name, country), None)

df['Account Owner'] = df.apply(assign_owner, axis=1)
df['CS Owner'] = df['Account Owner']

# Add the Billing Country field with "United States"
df['Billing Country'] = 'United States'

# Save the updated DataFrame back to a CSV file
df.to_csv('updated_csv_file.csv', index=False)
