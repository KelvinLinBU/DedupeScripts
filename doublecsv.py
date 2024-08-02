import pandas as pd
from fuzzywuzzy import fuzz
import re

# Helper function to normalize text
def normalize_text(text):
    if pd.isna(text):
        return ''
    return str(text).strip().lower()

# Helper function to remove symbols, non-letters, and text within parentheses
def clean_text(text):
    if pd.isna(text):
        return ''
    text = re.sub(r'\([^)]*\)', '', text)  # Remove text within parentheses
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove all non-letter characters
    return text.strip().lower()

# Load the CSV files
csv1 = pd.read_csv('C:/Users/klin/OneDrive - PTC/DedupeScripts/SchoolData.csv')
csv2 = pd.read_csv('C:/Users/klin/OneDrive - PTC/DedupeScripts/dupes_grouped2.csv')

# Check column names to ensure they match the expected ones
print("Columns in CSV1:", csv1.columns)
print("Columns in CSV2:", csv2.columns)

# Function to perform fuzzy matching and move entries
def fuzzy_match_and_move(csv1, csv2, start_index=0, threshold=94):
    rows_to_remove = []

    # Ensure 'Group ID' and 'Group Size' columns exist in csv2
    if 'Group ID' not in csv2.columns:
        csv2['Group ID'] = range(1, len(csv2) + 1)
    if 'Group Size' not in csv2.columns:
        csv2['Group Size'] = 1

    # Iterate through each row in the first CSV starting from the specified index
    for index1, row1 in csv1.iloc[start_index:].iterrows():
        try:
            best_match = None
            best_score = 0
            best_index2 = None

            # Skip rows where the representative account name is a single word
            if len(str(row1.get('Account Name', '')).split()) <= 1:
                continue

            # Normalize and clean the billing state and city for the current row in csv1
            state1 = normalize_text(row1.get('Billing State/Province', ''))
            city1 = normalize_text(row1.get('Billing City', ''))

            # Clean the account name for fuzzy matching
            account_name1 = clean_text(row1.get('Account Name', ''))

            # Iterate through each row in the second CSV
            for index2, row2 in csv2.iterrows():
                # Normalize and clean the billing state and city for the current row in csv2
                state2 = normalize_text(row2.get('Billing State/Province', ''))
                city2 = normalize_text(row2.get('Billing City', ''))

                # Clean the account name for fuzzy matching
                account_name2 = clean_text(row2.get('Account Name', ''))

                # Compute the fuzzy match score
                score = fuzz.ratio(account_name1, account_name2)

                # Check if score is above threshold and other conditions for exact matches
                if (score > threshold and state1 == state2):
                    if score > best_score:
                        best_match = row2
                        best_score = score
                        best_index2 = index2

            # If no match is found
            if best_match is None:
                print(f"No match found for institution: {row1.get('Account Name', '')}")

            # If a best match is found and best_score > 0 to avoid false positives
            if best_match is not None and best_score > 0:
                # Create a new row combining data from both CSVs
                new_row = pd.Series({col: str(row1.get(col, best_match[col])) if pd.notna(row1.get(col, None)) else str(best_match[col]) for col in best_match.index})
                new_row['Engineering University'] = str(row1.get('Engineering University', ''))

                # Keep Account ID blank
                new_row['Account ID'] = ''

                # Add the representative account ID to the new entry
                new_row['Group ID'] = best_match['Group ID']
                # Update the group size in the new entry
                new_row['Group Size'] = best_match['Group Size'] + 1

                # Update the group size for all entries with the same Group ID in csv2
                csv2.loc[csv2['Group ID'] == best_match['Group ID'], 'Group Size'] += 1

                # Update the Engineering University for all entries with the same Group ID in csv2
                csv2.loc[csv2['Group ID'] == best_match['Group ID'], 'Engineering University'] = new_row['Engineering University']

                # Insert the new row into csv2
                csv2 = pd.concat([csv2.iloc[:best_index2], pd.DataFrame([new_row]), csv2.iloc[best_index2:]]).reset_index(drop=True)

                # Mark the row for removal from the first CSV
                rows_to_remove.append(index1)

                print("Inserted:")
                print(new_row["Account Name"])
                print("Best score: " + str(best_score))

                # Save the updated CSV files after each match
                csv1.to_csv('C:/Users/klin/OneDrive - PTC/DedupeScripts/updated_SchoolDatav2.csv', index=False)
                csv2.to_csv('C:/Users/klin/OneDrive - PTC/DedupeScripts/updated_dupes_groupedv2.csv', index=False)
        except Exception as e:
            print(f"Error processing row {index1}: {e}")

    # Remove matched rows from csv1
    csv1 = csv1.drop(rows_to_remove).reset_index(drop=True)

    return csv1, csv2

# Starting index (line number to start processing from)
start_index = 100  # Example: start from the 101st row

# Perform the fuzzy matching and move entries starting from the specified index
csv1, csv2 = fuzzy_match_and_move(csv1, csv2, start_index=start_index)

# Final save to ensure any last changes are saved
csv1.to_csv('C:/Users/klin/OneDrive - PTC/DedupeScripts/updated_SchoolDatav2.csv', index=False)
csv2.to_csv('C:/Users/klin/OneDrive - PTC/DedupeScripts/updated_dupes_groupedv2.csv', index=False)

