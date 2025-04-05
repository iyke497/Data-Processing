import pandas as pd
import argparse

def json_to_excel(input_file, output_file):
    """
    Reads a JSON file and writes the data to an Excel file.
    
    Parameters:
        input_file (str): Path to the input JSON file.
        output_file (str): Path for the output Excel file.
    """
    try:
        # Read JSON file into a DataFrame
        df = pd.read_json(input_file)
        
        # Write the DataFrame to an Excel file
        df.to_excel(output_file, index=False)
        
        print(f"Successfully converted {input_file} to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Convert a JSON file to an Excel file using pandas.")
    parser.add_argument('input_file', help="Path to the input JSON file")
    parser.add_argument('output_file', help="Path to the output Excel file (e.g., output.xlsx)")
    
    args = parser.parse_args()
    
    json_to_excel(args.input_file, args.output_file)
