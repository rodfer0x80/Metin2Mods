import csv
import os
from pathlib import Path

class Table:
    def __init__(self, inputFilename: Path = "", outputFilename: Path = ""):
        self.inputFilename = inputFilename
        self.outputFilename = outputFilename


    def makeSeparator(self, headers, col_widths, sep_left='+', sep_mid='+', sep_right='+'):
        return (
            sep_left
            + '+'.join('-' * (col_widths[h] + 2) for h in headers)
            + sep_right
        )

    def print(self):
        if self.inputFilename and self.outputFilename:
            self.prettyPrintFromFileToFile()
        elif self.inputFilename:
            self.prettyPrintFromFileToStdout()


    def prettyPrintFromFileToFile(self):
        output = ""
        with open(self.inputFilename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if not rows:
            print('No data found in output file.')
            return
        headers = reader.fieldnames
        col_widths = {
            h: max(len(h), max(len(str(r[h])) for r in rows)) for h in headers
        }
        output += self.makeSeparator(headers=headers, col_widths=col_widths)
        header_row = (
            '| ' + ' | '.join(f'{h:<{col_widths[h]}}' for h in headers) + ' |'
        )
        output += header_row
        output += self.makeSeparator(headers=headers, col_widths=col_widths)
        for r in rows:
            row_str = (
                '| '
                + ' | '.join(f'{r[h]:<{col_widths[h]}}' for h in headers)
                + ' |'
            )
            output += row_str
            output += self.makeSeparator(headers=headers, col_widths=col_widths)
        with open(self.outputFilename, 'w') as h:
            h.write(output)
        h.flush()


    def prettyPrintFromFileToStdout(self) -> None:
        with open(self.inputFilename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if not rows:
            print('No data found in output file.')
            return
        headers = reader.fieldnames
        col_widths = {
            h: max(len(h), max(len(str(r[h])) for r in rows)) for h in headers
        }
        print(self.makeSeparator(headers=headers, col_widths=col_widths))
        header_row = (
            '| ' + ' | '.join(f'{h:<{col_widths[h]}}' for h in headers) + ' |'
        )
        print(header_row)
        print(self.makeSeparator(headers=headers, col_widths=col_widths))
        for r in rows:
            row_str = (
                '| '
                + ' | '.join(f'{r[h]:<{col_widths[h]}}' for h in headers)
                + ' |'
            )
            print(row_str)
            print(self.makeSeparator(headers=headers, col_widths=col_widths))

