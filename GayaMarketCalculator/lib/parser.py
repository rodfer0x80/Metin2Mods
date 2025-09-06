import csv
import os
from pathlib import Path


def _runGayaMarketCalculator(
    spiritStoneCost: int, itemCost: int, gayaCost: int
) -> float:
    gayaValue = itemCost / gayaCost

    refineChance = 0.6
    rawStoneStackSize = 200
    gayaOutcomePerRefine = 3
    rawStoneUsedPerRefine = 30

    gayaPerRefine = gayaOutcomePerRefine * refineChance
    rawStoneUsedPerGaya = rawStoneUsedPerRefine / gayaPerRefine
    gayaPerRawStoneStack = rawStoneStackSize / rawStoneUsedPerGaya
    gayaValuePerRawStoneStack = gayaPerRawStoneStack * gayaValue

    spiritStonePerRawStoneStack = rawStoneStackSize / rawStoneUsedPerRefine
    spiritStoneCostPerRawStoneStack = (
        spiritStonePerRawStoneStack * spiritStoneCost
    )

    maxRawStoneStackCost = (
        gayaValuePerRawStoneStack - spiritStoneCostPerRawStoneStack
    )

    return maxRawStoneStackCost


def runGayaMarketCalculator(
    spiritStoneCost: int, itemsIn: list[dict]
) -> list[dict]:
    itemsOut = []
    for item in itemsIn:
        if item['Item Cost'] == "0":
            continue
        maxRawStoneStackCost = _runGayaMarketCalculator(
            spiritStoneCost, int(item['Item Cost']), int(item['Gaya Cost'])
        )
        itemsOut.append(
            {
                'Item Name': item['Item Name'],
                'Max Raw Stone Cost': round(maxRawStoneStackCost, 2),
                'Item Cost': item['Item Cost'],
            }
        )
    itemsOut.sort(key=lambda x: float(x['Max Raw Stone Cost']), reverse=True)
    return itemsOut


def readCSV(filename: Path) -> tuple[int, list[dict]]:
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # First row is the Spirit Stone Cost
    spiritStoneRow = rows[0]
    spiritStoneCost = int(spiritStoneRow['Item Cost'])

    items = rows[1:]

    return spiritStoneCost, items


def writeCSV(filename: Path, itemsOut: list[dict]) -> None:
    fieldnames = [
        'Item Name',
        'Max Raw Stone Cost',
        'Item Cost',
    ]
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(itemsOut)


def parseInput(inputFilename: Path, outputFilename: Path) -> None:
    print('[*] Reading input data → ./data/input.csv')
    spiritStoneCost, itemsIn = readCSV(inputFilename)
    itemsOut = runGayaMarketCalculator(spiritStoneCost, itemsIn)
    print(f'[*] Processed {len(itemsIn)} items')
    print('[*] Writting output data → ./data/output.csv')
    writeCSV(outputFilename, itemsOut)


if __name__ == '__main__':
    DATA_INPUT_CSV = Path(os.environ.get('DATA_INPUT_CSV', './data/input.csv'))
    DATA_OUTPUT_CSV = Path(
        os.environ.get('DATA_OUTPUT_CSV', './data/output.csv')
    )
    parseInput(DATA_INPUT_CSV, DATA_OUTPUT_CSV)
