import pandas as pd
import os
import re

# Path to the directory containing Excel files and subdirectories
xlsx_dir = '/home/coulonn/Documents/Piste/duSoleilaSMH/consumption/xlsx/'

# Create a list to hold all .xlsx files found in subdirectories
excel_files = []

# Walk through the directory and its subdirectories
for root, dirs, files in os.walk(xlsx_dir):
    for file in files:
        if file.endswith('.xlsx'):
            excel_files.append(os.path.join(root, file))

# Loop through each Excel file found
for full_excel_path in excel_files:
    # Get the base name of the Excel file (without the path and extension)
    base_file_name = os.path.splitext(os.path.basename(full_excel_path))[0]

    # Extract the first long number (before '20XX') from the file name
    match = re.search(r'(\d+)\s+20', base_file_name)
    if match:
        directory_name = match.group(1)  # The extracted number (e.g., '19311143228790')
    else:
        print(f"Could not find the number before '20XX' in the file name: {base_file_name}")
        continue  # Skip this file if it doesn't match the pattern

    # Create the output directory using the extracted number
    csv_output_dir = f'/home/coulonn/Documents/Piste/duSoleilaSMH/consumption/csv/{directory_name}/'
    if not os.path.exists(csv_output_dir):
        os.makedirs(csv_output_dir)

    # Replace spaces in the base file name with underscores
    base_file_name = base_file_name.replace(" ", "_")

    # Read all sheets at once
    all_sheets = pd.read_excel(full_excel_path, sheet_name=None)

    # Loop through the sheets and save each one as a CSV
    for sheet_name, sheet_data in all_sheets.items():
        # Replace special characters in sheet names (e.g., é -> e)
        sheet_name = sheet_name.replace("é", "e")

        # Form the new file name as "old_file_name_sheet_name.csv"
        csv_file_name = f"{base_file_name}_{sheet_name}.csv"

        # Save each sheet to a CSV file in the dynamically created directory
        csv_file_path = os.path.join(csv_output_dir, csv_file_name)
        sheet_data.to_csv(csv_file_path, index=False)

        print(f"Saved {csv_file_path}")
