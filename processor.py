import re
import json

def extract_lines(file_path):
    """
    Extracts rows from a markdown file that match the following format:
    | CODE | PROJECT NAME | STATUS/TYPE | AMOUNT |
    
    Returns:
        A list of dictionaries with the extracted values.
    """
    # This regex looks for lines starting with '|' and extracts:
    # 1. The code (assumed to start with 'ERGP' followed by digits)
    # 2. The project name (any text until the next '|')
    # 3. The status/type (any text until the next '|')
    # 4. The amount (digits and commas)
    pattern = re.compile(
        r'^\|\s*(ERGP\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([\d,]+)\s*\|'
    )
    extracted = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                code, project_name, status, amount = match.groups()
                extracted.append({
                    'Code': code,
                    'Project Name': project_name,
                    'Status/Type': status,
                    'Amount': amount
                })
    return extracted

if __name__ == "__main__":
    # Assuming the markdown files are named output_chunk_1.md to output_chunk_5.md.
    for i in range(1, 6):
        file_path = f"output_chunk_{i}.md"
        extracted_data = extract_lines(file_path)
        
        # Write the extracted JSON data to a corresponding output file.
        output_file = f"output_chunk_{i}.json"
        with open(output_file, "w", encoding="utf-8") as outfile:
            json.dump(extracted_data, outfile, indent=2)
        
