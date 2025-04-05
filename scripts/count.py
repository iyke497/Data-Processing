import json

def count_projects_in_file(json_file):
    """Opens a JSON file and returns the count of project dictionaries."""
    with open(json_file, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    return len(projects)

if __name__ == "__main__":
    # List of JSON files (adjust file names if necessary)
    json_files = [f"2025_act_chunk_{i}.json" for i in range(1, 6)]
    
    for file in json_files:
        count = count_projects_in_file(file)
        print(f"{file} contains {count} projects.")



# output_chunk_1.json contains 691 projects.                                                                                                                                                  
# output_chunk_2.json contains 1094 projects.                    
# output_chunk_3.json contains 1350 projects.                                       
# output_chunk_4.json contains 601 projects.                                                                                                                                                  
# output_chunk_5.json contains 526 projects.

# 2025_act_chunk_1.json contains 1542 projects.        
# 2025_act_chunk_2.json contains 2066 projects.                                                                                          
# 2025_act_chunk_3.json contains 2460 projects.        
# 2025_act_chunk_4.json contains 1773 projects.                                                                                                                                   
# 2025_act_chunk_5.json contains 683 projects. 