import pandas as pd
import os

file_path = '/Users/macbookair/airflow/data/loan_approval_data.csv'  
df_with_errors = pd.read_csv(file_path)

# Create the folder 'raw_data' in the specified directory if it doesn't exist
output_folder = '/Users/macbookair/airflow/raw_data'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Total number of rows in the dataset
total_rows = df_with_errors.shape[0]

# Total number of files to split into (10 files)
num_files = 10

# Calculate the base number of rows per file and any remaining rows
rows_per_file = total_rows // num_files  # Each file should have 1000 rows
extra_rows = total_rows % num_files  # This gives any extra rows that need to be distributed

# Start splitting the dataset
start_row = 0
for i in range(num_files):
    if i < extra_rows:
        # Distribute one extra row to the first 'extra_rows' files if there are any
        end_row = start_row + rows_per_file + 1
    else:
        end_row = start_row + rows_per_file
    
    # Extract the subset of the dataset for this file
    split_df = df_with_errors.iloc[start_row:end_row]
    
    # Save the split file with leading zeros in the name (split_file_001.csv)
    split_file_path = os.path.join(output_folder, f'split_file_{i+1:03}.csv')
    split_df.to_csv(split_file_path, index=False)
    
    # Move the starting row forward for the next split
    start_row = end_row

print(f"All {num_files} files saved in '{output_folder}' folder, with a total of {total_rows} rows.")

