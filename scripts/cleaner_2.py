#!/usr/bin/env python3
import json
import math
import re

def is_nan(value):
    """
    Returns True if the value is considered empty (None or an actual NaN).
    """
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return False

def check_column_A(value):
    """
    Validates that Column A contains a string that starts with "ERGP"
    followed by one or more alphanumeric characters.
    
    For example, "ERGP26102464" is valid.
    """
    if isinstance(value, str):
        # Strip any extra whitespace and perform a full regex match.
        return bool(re.fullmatch(r'ERGP[A-Za-z0-9]+', value.strip()))
    return False

def check_column_C(value):
    """
    Checks that Column C (Status) is one of the allowed values.
    Allowed values (case-insensitive):
      - Empty (NaN/None)
      - "NEW"
      - "ONGOING" or "ON-GOING"
    """
    allowed = {"NEW", "ONGOING", "ON-GOING"}
    if is_nan(value):
        return True
    if isinstance(value, str) and value.strip().upper() in allowed:
        return True
    return False

def check_column_D(value):
    """
    Ensures that Column D (Amount) contains an integer value.
    The amount must be convertible to an integer and be at least 500,000.
    """
    try:
        int_value = int(value)
    except (ValueError, TypeError):
        return False
    return int_value >= 500000

def validate_file(filename):
    """
    Loads the JSON file and validates each row (except the header row).
    Checks:
      - Column A must match the pattern "ERGP" followed by alphanumerics.
      - Column C must be empty or one of the allowed statuses.
      - Column D must be an integer and >= 500000.
    
    Returns a dictionary with lists of row numbers that have errors.
    (Row numbers are provided as 1-indexed values corresponding to the file’s rows.)
    """
    with open(filename, "r") as f:
        data = json.load(f)
    
    error_rows_a = []
    error_rows_c = []
    error_rows_d = []
    
    for i, row in enumerate(data):
        # Skip header row (assumed if Column A is "CODE")
        if row.get("A") == "CODE":
            continue
        
        row_number = i + 1  # use i+1 to match file row numbers (including header if desired)
        
        # Validate Column A
        val_a = row.get("A")
        if not check_column_A(val_a):
            error_rows_a.append(row_number)
        
        # Validate Column C
        val_c = row.get("C")
        if not check_column_C(val_c):
            error_rows_c.append(row_number)
        
        # Validate Column D
        val_d = row.get("D")
        if not check_column_D(val_d):
            error_rows_d.append(row_number)
    
    return {
        "Column A errors": error_rows_a,
        "Column C errors": error_rows_c,
        "Column D errors": error_rows_d,
    }

def main():
    # List the file names for your five JSON files.
    files = ["validated_files/1.json", "validated_files/2.json", "validated_files/3.json", "validated_files/4.json", "validated_files/5.json"]
    
    for filename in files:
        errors = validate_file(filename)
        print(f"File: {filename}")
        if errors["Column A errors"]:
            print(f"  Rows with issues in Column A: {errors['Column A errors']}")
        else:
            print("  Column A passed for all rows.")
        if errors["Column C errors"]:
            print(f"  Rows with issues in Column C: {errors['Column C errors']}")
        else:
            print("  Column C passed for all rows.")
        if errors["Column D errors"]:
            print(f"  Rows with issues in Column D: {errors['Column D errors']}")
        else:
            print("  Column D passed for all rows.")
        print("-----")

if __name__ == "__main__":
    main()
