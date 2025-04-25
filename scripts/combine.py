import pandas as pd

# List of Excel file names in the desired order.
excel_files = ["validated_files/1.xlsx", "validated_files/2.xlsx", "validated_files/3.xlsx", "validated_files/4.xlsx", "validated_files/5.xlsx"]

# Read each Excel file into a DataFrame.
dfs = [pd.read_excel(file) for file in excel_files]

# Concatenate all DataFrames along rows. 
# 'ignore_index=True' ensures that the new DataFrame has a continuous index.
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a new Excel file.
combined_df.to_excel("combined.xlsx", index=False)

print("Excel files have been successfully combined into 'combined.xlsx'.")
