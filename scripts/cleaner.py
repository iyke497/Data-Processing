#!/usr/bin/env python3
import json
import re
import math

def not_nan(value):
    """
    Returns True if the value is not None or a NaN float.
    """
    if value is None:
        return False
    if isinstance(value, float) and math.isnan(value):
        return False
    return True

def split_combined_cell_A(rows):
    """
    Process rows where column A contains a combined value of:
      [code] [project name] [status] [amount].
      
    Pattern example:
      "ERGP4224392 INFRASTRUCTURAL DEVELOPMENT IN NAF BASES NEW 9,180,000,000"
      
    This function splits the string using a regex and updates:
      - Column A with the code,
      - Column B with the project name,
      - Column C with the status,
      - Column D with the amount.
    """
    # Regex explanation:
    # ^(ERGP[A-Za-z0-9]+) : Group 1 matches a code starting with ERGP
    # \s+                : One or more whitespace characters
    # (.*?)              : Group 2 (non-greedy): the project name
    # \s+(\w+)\s+       : Group 3: status (a word), surrounded by whitespace
    # ([\d,]+)\s*$      : Group 4: amount (digits and commas) until the end of the string
    pattern_A = re.compile(r'^(ERGP[A-Za-z0-9]+)\s+(.*?)\s+(\w+)\s+([\d,]+)\s*$')
    
    for row in rows:
        val_A = row.get("A")
        if isinstance(val_A, str):
            match = pattern_A.match(val_A)
            if match:
                code, project_name, status, amount = match.groups()
                row["A"] = code.strip()
                row["B"] = project_name.strip()
                row["C"] = status.strip()
                row["D"] = amount.strip()
    return rows

def split_combined_cell_B(rows):
    """
    Process rows where column B (project name column) contains extra appended data,
    such as a status and an amount.
    
    Pattern example:
      "REHABITATION OF OFF PTF ROAD AT ORANGE CLOSE HAYIN BANKI KADUNA
       
       NEW 100,000,000"
       
    This regex splits:
      - Group 1: The proper project name,
      - Group 2: The status,
      - Group 3: The amount.
    
    The function updates:
      - Column B with the cleaned project name,
      - Column C with the status,
      - Column D with the amount.
    """
    # DOTALL flag lets the dot match newline characters.
    pattern_B = re.compile(r'^(.*?)\s+(\w+)\s+([\d,]+)\s*$', re.DOTALL)
    
    for row in rows:
        val_B = row.get("B")
        if isinstance(val_B, str):
            match = pattern_B.match(val_B)
            if match:
                project_name, status, amount = match.groups()
                row["B"] = project_name.strip()
                row["C"] = status.strip()
                row["D"] = amount.strip()
    return rows

def main():
    # Load your JSON file (adjust the filename as needed)
    with open("2001-2500_filtered.json", "r") as infile:
        data = json.load(infile)
    
    # First, process column A if it has combined code and project info.
    data = split_combined_cell_A(data)
    # Next, process column B if it contains appended status and amount.
    data = split_combined_cell_B(data)
    
    # Write the cleaned and updated data to a new JSON file.
    with open("2001-2500_2xcleaned.json", "w") as outfile:
        json.dump(data, outfile, indent=2)

if __name__ == "__main__":
    main()
