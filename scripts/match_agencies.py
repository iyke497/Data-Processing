#!/usr/bin/env python3
import json
import re
import math

def not_nan(value):
    """
    Checks if the value is not considered "empty".
    Treats None or a NaN float as empty.
    """
    if value is None:
        return False
    if isinstance(value, float) and math.isnan(value):
        return False
    return True

def is_header_row(row):
    """
    Determines if the row is a header row by verifying that only keys A and B
    contain non-empty values.
    """
    non_empty_keys = [key for key, val in row.items() if not_nan(val)]
    return set(non_empty_keys) == {"A", "B"}

def a_matches_regex(value):
    """
    Checks if the given value (converted to a string) exactly matches a 9-digit number.
    """
    return bool(re.fullmatch(r'\d{9}', str(value)))

def process_rows(rows):
    """
    Processes the list of row dictionaries.
    
    - If a header row (only A and B are non-empty) is encountered, updates
      the stored header.
    - For non-header rows, if the value of key A starts with "ERGP" and a header
      has already been stored, it inserts the stored values into columns E and F.
    """
    stored_header = None  # To store (A_value, B_value)
    
    for row in rows:
        if is_header_row(row):
            # Update stored_header on every header row.
            # Check if A matches exactly 9 digits.
            if a_matches_regex(row["A"]):
                stored_header = (row["A"], row["B"])
            else:
                stored_header = (row["A"], row["B"])
        else:
            # For non-header rows, check if A is a string starting with "ERGP".
            a_val = row.get("A")
            if stored_header and isinstance(a_val, str) and a_val.startswith("ERGP"):
                row["E"], row["F"] = stored_header
    return rows

def main():
    # Load your JSON file (replace 'input.json' with your actual filename).
    with open("chunk_5.json", "r") as infile:
        data = json.load(infile)
    
    # Process the rows using our transformation rules.
    updated_data = process_rows(data)
    
    # Write the updated data to a new JSON file.
    with open("chunk_5_matched.json", "w") as outfile:
        json.dump(updated_data, outfile, indent=2)

if __name__ == "__main__":
    main()
