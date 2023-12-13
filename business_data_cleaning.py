import csv


# Function to remove 'u' prefix from a string value
def remove_u_prefix(value):
    if value.startswith("u'") or value.startswith('u"'):
        return value[1:]
    return value


# Open the original CSV file for reading and the new file for writing
# Make sure you have renamed the original file to business.csv and placed it in the same folder as this script
with open("business.csv", "r", encoding="utf-8") as infile, open(
    "business_new.csv", "w", newline="", encoding="utf-8"
) as outfile:
    # Create a CSV reader and writer
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Process each row in the CSV file
    for row in reader:
        new_row = [remove_u_prefix(cell) for cell in row]
        writer.writerow(new_row)
