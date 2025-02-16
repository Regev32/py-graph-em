import csv
import os
import shutil


def remove(input_csv_path, strings_to_remove):
    # Determine directory and backup file path.
    directory = os.path.dirname(input_csv_path)
    backup_csv_path = os.path.join(directory, "donor_becup.csv")

    # Create a backup copy of donor.csv
    shutil.copy(input_csv_path, backup_csv_path)
    print(f"Backup created: {backup_csv_path}")

    # Dictionary to count removals for each substring.
    removal_counts = {substr: 0 for substr in strings_to_remove}

    updated_rows = []

    # Read the original donor.csv
    with open(input_csv_path, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for row in reader:
            # Process only if the row has at least 2 columns.
            if len(row) >= 2:
                # Split the second column by '^'
                elements = row[1].split('^')
                new_elements = []
                for element in elements:
                    remove_flag = False
                    # Check if element contains any substring from strings_to_remove.
                    for substr in strings_to_remove:
                        if substr in element:
                            removal_counts[substr] += 1
                            remove_flag = True
                    if not remove_flag:
                        new_elements.append(element)
                # Reassemble the second column.
                row[1] = "^".join(new_elements)
            # Add (modified or not) the row to our updated_rows list.
            updated_rows.append(row)

    # Overwrite donor.csv with the updated rows.
    with open(input_csv_path, "w", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(updated_rows)

    # Print summary of removals for each substring.
    print("\nRemoval summary:")
    for substr, count in removal_counts.items():
        print(f"{substr}: removed {count}")


# Example usage:
if __name__ == "__main__":
    donor_csv_path = "data/subjects/donor.csv"
    strings_to_remove = ['DRBX', 'DRB3','DRB4','DRB5','DQA1','DPA1','DPB1']
    remove(donor_csv_path, strings_to_remove)
