# Scripts/xlxs_to_csv.py

import pandas as pd

# Load the Excel file
excel_file = './data/raw/Interview task for Position 9954496.xlsx'

print(f"Opening xlxs file: {excel_file}")

# Load all sheet names
sheet_names = pd.ExcelFile(excel_file).sheet_names

# Loop through sheets and save each as a CSV
for sheet in sheet_names:
    # Clean the sheet name for use as a filename
    safe_sheet_name = "".join(c if c.isalnum() or c in " -_." else "_" for c in sheet)

    print(f"Converting {safe_sheet_name} to csv...")

    # Read and convert sheet to csv file
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.to_csv(f"data/raw/{safe_sheet_name}.csv", index=False)

    print(f"Successfully converted {safe_sheet_name} to csv!")

print("All sheets sucessfully converted to csvs!")