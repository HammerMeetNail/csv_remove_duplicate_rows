import argparse
from collections import OrderedDict
import csv


def remove_duplicates(input_csv_path):
    """
    Opens a CSV file and returns back a dictionary of unique rows
    Columns should be: ID, chromosome_name, start_position, end_position, strand, padj, log2FoldChange
    """
    data = OrderedDict()
    total_rows = 0

    # Open CSV, iterate over each row, only insert unique rows into dictionary
    with open(input_csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)

        # First row is header, we should skip
        next(reader)  # skip first row

        for row in reader:
            total_rows += 1

            chromosome_name = row[1]
            start_position = row[2]
            end_position = row[3]
            strand = row[4]
            padj = row[5]
            log2FoldChange = row[6]

            key = f"{chromosome_name}{start_position}{end_position}{strand}{padj}{log2FoldChange}"

            data[key] = [
                chromosome_name,
                start_position,
                end_position,
                strand,
                padj,
                log2FoldChange,
            ]

    return data, total_rows


def write_output_csv(output_csv_path, data):
    """
    Accepts a dictionary of rows and writes a new CSV
    Columns should be: ID, chromosome_name, start_position, end_position, strand, padj, log2FoldChange
    """
    count = 1

    # Open a second output file and write only unique rows
    with open(output_csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")

        # First row, header
        header = [
            "'ID'",
            "'chromosome_name'",
            "'start_position'",
            "'end_position'",
            "'strand'",
            "'padj'",
            "'log2FoldChange'",
        ]
        writer.writerow(header)

        # Prepend a unique id and write to csv
        for key, value in data.items():
            writer.writerow([count] + value)

            count += 1

    return count - 1


# python3 remove_duplicates.py input.csv output.csv
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove duplicate rows from CSV file")
    parser.add_argument("input_csv_path", type=str, help="Path to source CSV")
    parser.add_argument("output_csv_path", type=str, help="Path to output CSV")
    args = parser.parse_args()

    unique_rows, total_rows = remove_duplicates(args.input_csv_path)
    rows_written = write_output_csv(args.output_csv_path, unique_rows)
    duplicates = total_rows - rows_written

    print(
        f"Looked at {total_rows} rows. Found {duplicates} duplicates. Found {rows_written} unique rows."
    )
