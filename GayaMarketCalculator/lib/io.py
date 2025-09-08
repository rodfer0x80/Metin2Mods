import csv
import os
from pathlib import Path

class IO:
    def __init__(self):
        return None 

    def readCSV(self, filename: Path) -> tuple[int, list[dict]]:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            items = list(reader)
        return items


    def writeCSV(self, filename: Path, itemsOut: list[dict]) -> None:
        fieldnames = [
            'Item Name',
            'Item Cost',
            'Max Raw Stone Cost',
            'Upfront Cost',
            'Profit Margin',
        ]
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(itemsOut)