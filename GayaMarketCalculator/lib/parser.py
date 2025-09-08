import csv
import os
from pathlib import Path

from .io import IO
from .config import Config

class Parser:
    def __init__(self, inputFilename: Path, outputFilename: Path, config: Config):
        self.inputFilename = inputFilename
        self.outputFilename = outputFilename
        self.config = Config()

    def _runGayaMarketCalculator(self, 
        itemCost: int, gayaCost: int
    ) -> tuple[float, float, float]:
        gayaValue = itemCost / gayaCost

        refineChance = 0.6
        rawStoneStackSize = 200
        gayaOutcomePerRefine = 3
        rawStoneUsedPerRefine = 30
        spiritStoneCost: int = self.config.spiritStoneCost
        profitMargin: float = self.config.profitMargin
        profitMarginMod = 1 - ( profitMargin / 100)

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
        ) * profitMarginMod

        upfrontCost = gayaCost * (
            (spiritStonePerRawStoneStack + maxRawStoneStackCost) / gayaPerRawStoneStack
        )

        return maxRawStoneStackCost, upfrontCost, profitMargin


    def runGayaMarketCalculator(self, itemsIn: list[dict]) -> list[dict]:
        itemsOut = []
        for item in itemsIn:
            if item['Item Cost'] == '0':
                continue
            maxRawStoneStackCost, upfrontCost, profitMargin = (
                self._runGayaMarketCalculator(
                    int(item['Item Cost']), int(item['Gaya Cost'])
                )
            )
            itemsOut.append(
                {
                    'Item Name': item['Item Name'],
                    'Item Cost': item['Item Cost'],
                    'Max Raw Stone Cost': round(maxRawStoneStackCost, 2),
                    'Upfront Cost': round(upfrontCost, 2),
                    'Profit Margin': f'{profitMargin}%',
                }
            )
        itemsOut.sort(key=lambda x: float(x['Max Raw Stone Cost']), reverse=True)
        return itemsOut

    def parse(self) -> None:
        io = IO()
        print(f'[*] Reading input data → {self.inputFilename}')
        itemsIn = io.readCSV(self.inputFilename)
        itemsOut = self.runGayaMarketCalculator(itemsIn)
        print(f'[*] Processed {len(itemsIn)} items')
        print(f'[*] Writting output data → {self.outputFilename}')
        io.writeCSV(self.outputFilename, itemsOut)
