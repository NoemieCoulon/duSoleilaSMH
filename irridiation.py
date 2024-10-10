import csv
from datetime import datetime
from collections import defaultdict

# File path to the CSV
file_path = "/home/coulonn/Documents/Piste/duSoleilaSMH/irridiation/MC_0_0.csv"

# Function to load and filter irradiation data by date range
# Function to load and filter irradiation data by date range
def irridiation(file_path, start_date, end_date):
    # Initialize a dictionary to store irradiation data per date and hour
    dictIrridiation = defaultdict(lambda: defaultdict(lambda: {'Total Irridiation': 0}))
    
    # Open the CSV file
    with open(file_path, 'r', encoding='utf-8', newline='') as file:
        # Skip the first 8 lines of metadata
        for _ in range(8):
            next(file)
        
        # Read the headers (ensuring proper formatting)
        headers = next(file).strip().replace("\t", "").replace("\r", "").split(",")
        
        # Initialize the CSV reader
        reader = csv.DictReader(file, fieldnames=headers)
        
        # Process each row in the CSV
        for row in reader:
            try:
                # Extract the timestamp from the first column
                date_str = row[headers[0]]
                
                # Convert the date string to a datetime object
                date_time = datetime.strptime(date_str, "%Y%m%d:%H%M")
                
                # Only consider the rows within the specified date range
                if start_date <= date_time < end_date:
                    # Check and log raw values before conversion
                    gb_raw = row[headers[1]]
                    gd_raw = row[headers[2]]
                    gr_raw = row[headers[3]]

                    # Check if the values are empty or not valid numbers, convert or default to 0
                    try:
                        gb = float(gb_raw) if gb_raw else 0
                        gd = float(gd_raw) if gd_raw else 0
                        gr = float(gr_raw) if gr_raw else 0
                    except ValueError:
                        print(f"Invalid value encountered in row: {row}")
                        gb, gd, gr = 0, 0, 0  # Default to zero if conversion fails
                    
                    # Store the total irradiation
                    total_irr = gb + gd + gr
                    dictIrridiation[date_time]['Total Irridiation'] = total_irr

            except ValueError as ve:
                # Catch any issues in date or float parsing and print an error message
                # print(f"Skipping row due to error: {ve}")
                continue
            except KeyError as ke:
                # Handle missing or incorrect column headers
                print(f"KeyError: {ke}")
            except Exception as e:
                # Generic exception handling for unexpected issues
                # print(f"Skipping row due to an unexpected error: {e}")
                continue
    return dictIrridiation

# # Function call with start and end date
# start_date = datetime(2023, 1, 1)
# end_date = datetime(2023, 1, 2)
# dictIrr = irridiation(file_path, start_date, end_date)

# # Retrieve the list of all irradiation values
# list_irr = [v['Total Irridiation'] for k, v in dictIrr.items()]

# # Print the list of irradiation values
