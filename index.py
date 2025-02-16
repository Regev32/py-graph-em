import csv


def update_first_column_with_numbering(input_csv_path):
    """
    Reads the CSV file from input_csv_path.
    For each row, replaces the first column with a sequential number starting at 1.
    Overwrites the original CSV with the updated rows.

    For example, if the original rows are:
        hjsdh,...
        kuayj,...
        kjaha,...
        husd,...
    They will become:
        1,...
        2,...
        3,...
        4,...
    """
    updated_rows = []

    # Read all rows from the original CSV.
    with open(input_csv_path, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for index, row in enumerate(reader, start=1):
            if row:  # Only process non-empty rows
                row[0] = str(index)
            updated_rows.append(row)

    # Overwrite the CSV with the updated rows.
    with open(input_csv_path, "w", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(updated_rows)

    print(f"Updated the first column with numbering in {input_csv_path}.")


# Example usage:
if __name__ == "__main__":
    donor_csv_path = "data/subjects/donor.csv"
    update_first_column_with_numbering(donor_csv_path)
