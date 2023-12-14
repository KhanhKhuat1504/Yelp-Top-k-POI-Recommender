import csv
import os

def split_csv(source_filepath, dest_folder, split_file_prefix, number_of_files=20):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Count total number of rows in the source file
    with open(source_filepath, 'r', newline='', encoding='utf-8') as source_file:
        row_count = sum(1 for row in csv.reader(source_file))

    # Calculate number of rows per file
    rows_per_file = row_count // number_of_files
    if row_count % number_of_files != 0:
        rows_per_file += 1

    with open(source_filepath, 'r', newline='', encoding='utf-8') as source_file:
        reader = csv.reader(source_file)
        for file_index in range(number_of_files):
            with open(os.path.join(dest_folder, f'{split_file_prefix}_{file_index + 1}.csv'), 
                      'w', newline='', encoding='utf-8') as dest_file:
                writer = csv.writer(dest_file)
                for row_index, row in enumerate(reader):
                    writer.writerow(row)
                    if row_index + 1 == rows_per_file:
                        break

# Example usage
split_csv('business_final.csv', 'business', 'small_academic_dataset_business')
