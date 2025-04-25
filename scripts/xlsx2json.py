import pandas as pd
import json
import sys
import string

def xlsx_to_json_with_letters(input_file, output_file):
    # Read the Excel file without treating the first row as headers
    df = pd.read_excel(input_file, header=None)
    
    # Determine the number of columns and create column names as A, B, C, ...
    n_cols = df.shape[1]
    # Use letters from the English alphabet (assumes n_cols <= 26)
    col_names = list(string.ascii_uppercase[:n_cols])
    df.columns = col_names

    # Convert the DataFrame to a list of dictionaries (each row becomes a dict)
    data = df.to_dict(orient="records")
    
    # Write the output to a JSON file
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Converted '{input_file}' to '{output_file}' with column keys: {col_names}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python xlsx_to_json_with_letters.py input_file.xlsx output_file.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    xlsx_to_json_with_letters(input_file, output_file)
