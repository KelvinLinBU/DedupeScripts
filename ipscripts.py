import csv
import requests

def lookup_institution(ip_address):
    try:
        url = f"https://whois.arin.net/rest/ip/{ip_address}.json"
        response = requests.get(url,verify=False)
        if response.status_code == 200:
            data = response.json()
            net = data.get('net', {})
            org_ref = net.get('orgRef', {})
            institution = org_ref.get('@name', 'Unknown Institution')
            return institution
        else:
            print(f"Failed to retrieve data for IP {ip_address}: {response.status_code}")
            return 'Unknown Institution'
    except Exception as e:
        print(f"Error processing IP {ip_address}: {e}")
        return 'Unknown Institution'

def process_csv(input_file, output_file, start_line):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        csv_reader = csv.DictReader(infile)
        fieldnames = csv_reader.fieldnames + ['Institution']
        csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Write the header to the output file
        csv_writer.writeheader()
        
        # Skip lines until the start_line
        for _ in range(start_line):
            next(csv_reader)
        
        # Process each row starting from the specified line
        for row in csv_reader:
            ip_address = row['IP Address']
            institution = lookup_institution(ip_address)
            row['Institution'] = institution
            csv_writer.writerow(row)
            print(f"Processed IP: {ip_address}, Institution: {institution}")

if __name__ == "__main__":
    input_file = "newip.csv"  # Replace with the path to your input file
    output_file = "newipsearched.csv"  # Replace with the desired output file path
    start_line =350   # Change this to the desired starting line
    
    process_csv(input_file, output_file, start_line)

    print(f"Updated CSV saved to {output_file}")
