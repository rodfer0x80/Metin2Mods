import csv
import os
from pathlib import Path


def prettyPrintOutput(filename: Path) -> None:
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print('No data found in output file.')
        return

    headers = reader.fieldnames
    col_widths = {
        h: max(len(h), max(len(str(r[h])) for r in rows)) for h in headers
    }

    def make_separator(sep_left='+', sep_mid='+', sep_right='+'):
        return (
            sep_left
            + '+'.join('-' * (col_widths[h] + 2) for h in headers)
            + sep_right
        )

    # top border
    print(make_separator())

    # header row
    header_row = (
        '| ' + ' | '.join(f'{h:<{col_widths[h]}}' for h in headers) + ' |'
    )
    print(header_row)

    # header separator
    print(make_separator())

    # rows
    for r in rows:
        row_str = (
            '| '
            + ' | '.join(f'{r[h]:<{col_widths[h]}}' for h in headers)
            + ' |'
        )
        print(row_str)
        print(make_separator())


if __name__ == '__main__':
    DATA_OUTPUT_CSV = Path(
        os.environ.get('DATA_OUTPUT_CSV', './data/output.csv')
    )
    prettyPrintOutput(DATA_OUTPUT_CSV)
