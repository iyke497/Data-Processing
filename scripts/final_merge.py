import json

# Load the JSON files
with open("json_files/2025_act_chunk_5.json", "r") as f_a:
    data_a = json.load(f_a)

with open("json_files/output_chunk_5.json", "r") as f_b:
    data_b = json.load(f_b)

# Build a set of project codes from file_a (reference)
codes_a = {item["Code"] for item in data_a if "Code" in item}

# Step 1: Compute segments from file_b.
# Each segment contains:
#   - 'prev_common': the last common project code encountered (or None if at the beginning)
#   - 'next_common': the next common project code (or None if at the end)
#   - 'missing_projects': the list of consecutive missing project entries (full dicts) from file_b.
segments = []
current_segment = {"prev_common": None, "missing_projects": []}

for project in data_b:
    code = project.get("Code")
    if code in codes_a:
        # When a common project is encountered:
        if current_segment["missing_projects"]:
            segments.append({
                "prev_common": current_segment["prev_common"],
                "next_common": code,
                "missing_projects": current_segment["missing_projects"]
            })
            # Reset segment with the current common as the new previous marker.
            current_segment = {"prev_common": code, "missing_projects": []}
        else:
            # Update the previous common marker if no missing projects have been collected.
            current_segment["prev_common"] = code
    else:
        # Project is missing in file_a; add it to the current block.
        current_segment["missing_projects"].append(project)

# If there's any remaining block at the end, append it.
if current_segment["missing_projects"]:
    segments.append({
        "prev_common": current_segment["prev_common"],
        "next_common": None,
        "missing_projects": current_segment["missing_projects"]
    })

# Step 2: Build an insertion mapping.
# Use "__BEGIN__" for missing projects at the very start.
insertions = {}
for segment in segments:
    marker = segment["prev_common"] if segment["prev_common"] is not None else "__BEGIN__"
    if marker in insertions:
        insertions[marker].extend(segment["missing_projects"])
    else:
        insertions[marker] = segment["missing_projects"]

# Step 3: Merge file_a and missing projects from file_b.
merged_list = []

# Insert missing projects at the beginning if any.
if "__BEGIN__" in insertions:
    for proj in insertions["__BEGIN__"]:
        merged_list.append(proj)

# Loop through file_a in order.
for project in data_a:
    merged_list.append(project)
    code = project.get("Code")
    if code in insertions:
        # Insert missing entries (one by one in their original order) right after this common project.
        for missing_proj in insertions[code]:
            merged_list.append(missing_proj)

# Write the merged list to a new JSON file.
output_filename = "merged_chunk_5.json"
with open(output_filename, "w") as f_out:
    json.dump(merged_list, f_out, indent=2)

print("Merged list saved to", output_filename)
