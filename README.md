# csv_remove_duplicate_rows
Remove duplicate rows from a CSV file. Creates a new tab delmited CSV.

# Prequisites
1. [Python 3](https://www.python.org/downloads/)
2. CSV file with the following columns, including single quotes:
    * 'ID'
    * 'chromosome_name'
    * 'start_position'
    * 'end_position'
    * 'strand'
    * 'padj'
    * 'log2FoldChange'

# Quickstart
```
python3 remove_duplicates.py input.csv output.csv
```

# Required Args
```
python3 remove_duplicates.py -h
usage: remove_duplicates.py [-h] input_csv_path output_csv_path

Remove duplicate rows from CSV file

positional arguments:
  input_csv_path   Path to source CSV
  output_csv_path  Path to output CSV

optional arguments:
  -h, --help       show this help message and exit
```