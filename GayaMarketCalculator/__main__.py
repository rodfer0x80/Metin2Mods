import os
import argparse
from pathlib import Path

from lib.parser import parseInput
from lib.printer import prettyPrintOutput


def main():
    argparser = argparse.ArgumentParser(
        description='Gaya Market Calculator CLI'
    )
    argparser.add_argument(
        'actions',
        nargs='+',
        choices=['parse', 'print'],
        help="Choose 'parse' to process input.csv → output.csv and/or 'print' to pretty-print output.csv",
    )
    argparser.add_argument(
        '-i',
        '--input',
        type=Path,
        default=Path(os.environ.get('DATA_INPUT_CSV', './data/input.csv')),
        help='Path to input CSV file (default: ./data/input.csv)',
    )
    argparser.add_argument(
        '-o',
        '--output',
        type=Path,
        default=Path(os.environ.get('DATA_OUTPUT_CSV', './data/output.csv')),
        help='Path to output CSV file (default: ./data/output.csv)',
    )

    args = argparser.parse_args()

    if 'parse' in args.actions:
        print('[*] Running Gaya Market Caculator...')
        parseInput(args.input, args.output)
        print('[*] Finished running GayaPriceCalculator')

    if 'print' in args.actions:
        prettyPrintOutput(args.output)
    
    return 0

if __name__ == '__main__':
    exit(main())
