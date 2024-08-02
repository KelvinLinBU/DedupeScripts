import pandas as pd

def filter_school_names(file_path, output_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Define keywords to filter out
    keywords = ['beauty', 'massage', 'barber', 'cosmetology', 'esthetician', 'nail', 'makeup', 'salon', 'therapy', 'culinary']

    # Create a case-insensitive filter
    pattern = '|'.join(keywords)
    mask = ~df['Account Name'].str.contains(pattern, case=False, na=False)

    # Apply the filter to the DataFrame
    filtered_df = df[mask]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_path, index=False)

# Example usage
input_file = 'C:/Users/klin/OneDrive - PTC/DedupeScripts/updated_SchoolDatav2.csv'  # Replace with the path to your input CSV file
output_file = 'schools_not_in_SF.csv'  # Replace with the desired output file path
filter_school_names(input_file, output_file)
