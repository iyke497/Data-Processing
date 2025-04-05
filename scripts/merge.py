import json

# Load file_a (reference) and file_b (to be merged)
with open("json_files/2025_act_chunk_3.json", "r") as f_a:
    data_a = json.load(f_a)
with open("json_files/output_chunk_3.json", "r") as f_b:
    data_b = json.load(f_b)

# Build a set of common project codes from file_a
codes_a = {item["Code"] for item in data_a if "Code" in item}

# Step 1. Compute segments from file_b.
# Each segment will have:
#   - 'prev_common': the last common code encountered (or None if missing at the very beginning)
#   - 'next_common': the next common code after the block (or None if at the end)
#   - 'missing_projects': list of consecutive missing projects (as dictionaries) from file_b.
segments = []
current_segment = {
    "prev_common": None,
    "missing_projects": []
}

for project in data_b:
    code = project.get("Code")
    if code in codes_a:
        # When we hit a common project:
        if current_segment["missing_projects"]:
            # End the current missing block, marking the current project as the next common.
            segments.append({
                "prev_common": current_segment["prev_common"],
                "next_common": code,
                "missing_projects": current_segment["missing_projects"]
            })
            # Reset current segment, and update the previous common marker.
            current_segment = {"prev_common": code, "missing_projects": []}
        else:
            # No missing project encountered yet; simply update the marker.
            current_segment["prev_common"] = code
    else:
        # This project is missing from file_a; add it to the current block.
        current_segment["missing_projects"].append(project)

# If there's a remaining block at the end, append it.
if current_segment["missing_projects"]:
    segments.append({
        "prev_common": current_segment["prev_common"],
        "next_common": None,
        "missing_projects": current_segment["missing_projects"]
    })

# Step 2. Build a dictionary for insertion.
# The key will be the "prev_common" marker.
# We'll use a special key "__BEGIN__" for segments with no previous common (i.e. to insert at the beginning).
insertions = {}

for segment in segments:
    marker = segment["prev_common"] if segment["prev_common"] is not None else "__BEGIN__"
    if marker in insertions:
        insertions[marker].extend(segment["missing_projects"])
    else:
        insertions[marker] = segment["missing_projects"]

# Step 3. Build the merged list.
merged_list = []

# If there are missing projects to insert at the beginning, add them.
if "__BEGIN__" in insertions:
    for proj in insertions["__BEGIN__"]:
        merged_list.append(proj)

# Iterate through file_a (reference) in order.
for project in data_a:
    merged_list.append(project)
    code = project.get("Code")
    # If there are missing projects mapped to this common code, insert them one by one.
    if code in insertions:
        for missing_proj in insertions[code]:
            merged_list.append(missing_proj)

# For demonstration, show some information:
print("Total projects in merged list:", len(merged_list))
print("Number of segments detected:", len(segments))
print("\nA sample segment from file_b:")
if segments:
    sample = segments[0]
    print("Prev common:", sample["prev_common"])
    print("Next common:", sample["next_common"])
    print("Missing projects in this segment:", len(sample["missing_projects"]))
