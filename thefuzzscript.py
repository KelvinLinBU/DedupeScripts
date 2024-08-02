import pandas as pd
import re
from cleanfuncs import clean_account_names, capitalize_account_names, normalize_acronyms, remove_parentheses_content, remove_commas, update_owners
from thefuzz import process
from rankentries import rank_entries, rank_criteria  # Assuming rank_entries is in a separate file named rankentries.py
import uuid

owner1 = "Nick Cross"
owner2 = "Jess Barbera"

# Sample dictionary for location to owner mapping
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

def group_similar_entries(df, name_column, city_column, state_column, threshold=93):
    df[name_column] = df[name_column].astype(str)
    df[city_column] = df[city_column].astype(str)
    df[state_column] = df[state_column].astype(str)
    unique_entries = df[name_column].unique()
    grouped_entries = {}
    
    for entry in unique_entries:
        if entry not in grouped_entries:
            print(entry)
            similar_entries = process.extract(entry, unique_entries, limit=None)
            similar_entries = [item[0] for item in similar_entries if item[1] >= threshold]
            similar_df = df[df[name_column].isin(similar_entries)]
            
            # Filter similar entries by city and state/province similarity
            city_state_groups = similar_df.groupby([city_column, state_column])
            for (city, state), group in city_state_groups:
                if city or state:  # Only apply city/state matching if they are not both empty
                    representative_entry = rank_entries(group)[name_column]
                    for similar_entry in group[name_column].unique():
                        grouped_entries[similar_entry] = representative_entry
                else:
                    # For entries with empty city or state, allow them to be attached to any group
                    for similar_entry in similar_entries:
                        grouped_entries[similar_entry] = rank_entries(similar_df)[name_column]
    
    return grouped_entries

# Load the CSV file into a DataFrame
file_path = 'C:/Users/klin/OneDrive - PTC/DedupeScripts/report1721239013093.csv'
df = pd.read_csv(file_path)

print("Original DataFrame:")
print(df)

# Ensure 'Account Name', 'City', and 'State/Province' columns exist
column_name = 'Account Name'
city_column = 'Billing City'
state_column = 'Billing State/Province'
country_column = 'Billing Country'
acct_owner_column = 'Account Owner'
cs_owner_column = 'CS Owner'
if column_name not in df.columns or city_column not in df.columns or state_column not in df.columns:
    raise KeyError(f"Columns '{column_name}', '{city_column}', and '{state_column}' must be present in the DataFrame.")

# Data cleaning steps
df = capitalize_account_names(df, country_column)
df = capitalize_account_names(df, state_column)
df = update_owners(df, state_column, country_column, acct_owner_column, cs_owner_column, location_to_owner_USCanada )
df = remove_commas(df, column_name)
df = remove_parentheses_content(df, column_name)
df = clean_account_names(df, column_name)
df = normalize_acronyms(df, column_name)
df = capitalize_account_names(df, column_name)

# Get the grouped entries dictionary
grouped_entries = group_similar_entries(df, column_name, city_column, state_column)

# Replace entries with their representative entry
df['Representative Account Name'] = df[column_name].map(grouped_entries)

# Generate a unique Group ID for each representative account name
group_ids = {rep_name: str(uuid.uuid4()) for rep_name in df['Representative Account Name'].unique()}
df['Group ID'] = df['Representative Account Name'].map(group_ids)

ordered_rows = []

for representative, group_df in df.groupby('Representative Account Name'):
    if len(group_df) > 1:
        ranked_group_df = rank_entries(group_df)
        master_entry = group_df.loc[group_df.index == ranked_group_df.name]
        master_entry = master_entry.copy()  # Ensure we are working with a copy
        master_entry.loc[:, 'Reason'] = ranked_group_df['deciding_factor']
        group_df = group_df.drop(ranked_group_df.name)
        ordered_rows.append(master_entry)
        ordered_rows.append(group_df)
    else:
        ordered_rows.append(group_df)

final_df = pd.concat(ordered_rows).reset_index(drop=True)

# Remove the 'rank' and 'deciding_factor' columns if they exist
if 'rank' in final_df.columns:
    final_df = final_df.drop(columns=['rank'])
if 'deciding_factor' in final_df.columns:
    final_df = final_df.drop(columns=['deciding_factor'])

# Add a column to count the number of accounts in each group
final_df['Group Size'] = final_df.groupby('Representative Account Name')['Representative Account Name'].transform('count')

# Calculate the total number of duplicate accounts found
total_duplicates = final_df['Group Size'].sum() - final_df['Representative Account Name'].nunique()

# Save the final DataFrame to a new CSV file
output_path = 'C:/Users/klin/OneDrive - PTC/DedupeScripts/dupes_grouped2.csv'
final_df.to_csv(output_path, index=False)

print(f'Final grouped entries with duplicates count saved to {output_path}')
print(f'Total duplicates found: {total_duplicates}')
