import argparse
from collections import OrderedDict
import csv


def process_coordinates(reader):
    """
    Each row is single tab delimited string of three values
    """
    data = OrderedDict()
    total_rows = 0

    for raw_row in reader:
        total_rows += 1

        row = raw_row[0].split("\t")

        chromosome_name = row[0]
        start_position = row[1]
        end_position = row[2]

        key = f"{chromosome_name}{start_position}{end_position}"

        data[key] = [
            chromosome_name,
            start_position,
            end_position,
        ]

    return data, total_rows


def process_differential_coordinates(reader):
    """
    Each row is a list of 7 values
    """
    data = OrderedDict()
    total_rows = 0

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


def remove_duplicates(input_csv_path):
    """
    Opens a CSV file and returns back a dictionary of unique rows
    Columns should be: ID, chromosome_name, start_position, end_position, strand, padj, log2FoldChange
    """
    data = OrderedDict()
    total_rows = 0
    csv_type = ""

    # Open CSV, iterate over each row, only insert unique rows into dictionary
    with open(input_csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            # Check if CSV is Coordinates or Differential Coordinates
            if row[0] == "\ufeff'ID'":
                csv_type = "diff"
                break
            else:
                # Coordinates CSV
                csv_type = "coor"
                break

        if csv_type == "diff":
            data, total_rows = process_differential_coordinates(reader)
        elif csv_type == "coor":
            data, total_rows = process_coordinates(reader)
        else:
            print(
                "Something bad happened! Columns don't match coordinate or differential coordinate format"
            )

    return data, total_rows, csv_type


def write_output_csv(output_csv_path, data, csv_type):
    """
    Accepts a dictionary of rows and writes a new CSV
    Columns should be: ID, chromosome_name, start_position, end_position, strand, padj, log2FoldChange
    """
    count = 1

    # Open a second output file and write only unique rows
    with open(output_csv_path, "w", newline="") as csv_file:

        # First row, header
        if csv_type == "diff":
            writer = csv.writer(csv_file, delimiter=",")
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
        else:
            writer = csv.writer(csv_file, delimiter="\t")
            # Prepend a unique id and write to csv
            for key, value in data.items():
                writer.writerow(value)

                count += 1

    return count - 1


# python3 remove_duplicates.py input.csv output.csv
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove duplicate rows from CSV file")
    parser.add_argument("input_csv_path", type=str, help="Path to source CSV")
    parser.add_argument("output_csv_path", type=str, help="Path to output CSV")
    args = parser.parse_args()

    unique_rows, total_rows, csv_type = remove_duplicates(args.input_csv_path)
    rows_written = write_output_csv(args.output_csv_path, unique_rows, csv_type)
    duplicates = total_rows - rows_written

    print(
        f"Looked at {total_rows} rows. Found {duplicates} duplicates. Found {rows_written} unique rows."
    )
