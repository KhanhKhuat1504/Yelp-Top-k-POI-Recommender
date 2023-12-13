import csv
import re

def clean_field(field):
    # Remove b'' or u'' prefixes from the field
    field = re.sub(r"^[bu]{0,1}'", '', field)
    field = re.sub(r"'$", '', field)
    return field

with open('yelp_academic_dataset_business.csv', 'r', newline='', encoding='utf-8') as infile, \
     open('cleaned_yelp_academic_dataset_business.csv', 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        cleaned_row = [clean_field(field) for field in row]
        writer.writerow(cleaned_row)
