import json
import re
import sys

def filter_budget_code(input_file, output_file):
    # Load the JSON file
    with open(input_file, "r") as f:
        data = json.load(f)
    
    # Compile a regex pattern to match strings that start with ERGP followed by one or more digits.
    pattern = re.compile(r"^ERGP\d+")
    
    # Filter rows where the value in column "A" matches the pattern.
    filtered_rows = []
    match_count = 0
    for row in data:
        value = row.get("A")
        # Ensure value is a string before applying the regex.
        if isinstance(value, str) and pattern.match(value):
            filtered_rows.append(row)
            match_count += 1

    print("Number of rows with a valid budget code in column A:", match_count)
    
    # Save the filtered rows to the output file, preserving their order.
    with open(output_file, "w") as f:
        json.dump(filtered_rows, f, indent=2)
    print("Filtered JSON saved to", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_budget_code.py input_file.json output_file.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    filter_budget_code(input_file, output_file)
