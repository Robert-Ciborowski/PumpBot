# Name: Dummy Pump and Dump Model
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A dummy test class used for detecting whether a stock is a
#              pump and dump. Don't use this class for anything other than
#              testing! All it does is generate a random value as its
#              probability! (The probability of its output being true is
#              the decision threshold itself.)

# from __future__ import annotations
from typing import Dict, List
import numpy as np
import pandas as pd

from models.PumpAndDumpDetector import PumpAndDumpDetector
from util.Constants import SAMPLES_OF_DATA_TO_LOOK_AT


class SimplePumpAndDumpDetector(PumpAndDumpDetector):
    _NUMBER_OF_SAMPLES = SAMPLES_OF_DATA_TO_LOOK_AT
    volumeStdThreshold: float
    priceStdThreshold: float

    def __init__(self, volumeStdThreshold: float, priceStdThreshold: float):
        super().__init__()
        self.setClassificationThreshold(1.0)
        self.volumeStdThreshold = volumeStdThreshold
        self.priceStdThreshold = priceStdThreshold

    def detect(self, prices, volumes) -> float:
        if prices is None:
            return False

        if isinstance(prices, List) or isinstance(prices, np.ndarray):
            # The list better contain only floats...
            prices, volumes = self._turnListOfFloatsToInputData(prices, volumes, SimplePumpAndDumpDetector._NUMBER_OF_SAMPLES)

            if volumes is None or prices is None:
                return 0

            return self._detect(prices, volumes)
        else:
            print("SimplePumpAndDumpDetector detect() had its precondition "
                  "violated!")
            return False

    def _detect(self, prices, volumes) -> float:
        # volumeStd = volumes.std()
        #
        # if volumeStd >= 2.0e-08:
        #     return False

        pivot = int(len(prices) * 0.925)
        prices2 = prices.iloc[0 : pivot]
        std2 = prices2.std()

        if std2 > 8.0e-08:
            print("Not std2")
            print(std2)
            return 0

        prices3 = prices.iloc[pivot: len(prices)]
        std3 = prices3.std()

        if std3 > 4.0e-07:
            print("Not std3")
            return 0

        endOfPrices2 = prices2.iloc[-1] * 0.75 + prices2.iloc[-2] * 0.25
        max2 = prices2.max()

        if prices3.iloc[-1] > prices3.iloc[-2]:
            endOfPrices3 = prices3.iloc[-1]
        else:
            endOfPrices3 = prices3.iloc[-1] * 0.75 + prices3.iloc[-2] * 0.25

        greaterThan = endOfPrices3 > max2 * 1.015

        if not greaterThan:
            print("Not greater than")
            print(str(endOfPrices3) + " " + str(max2))
            return 0

        max3 = prices3.max()
        greaterThan2 = endOfPrices3 * 1.01 > max3

        if not greaterThan2:
            print("Not greater than 2")
            return 0

        # lessThan = endOfPrices3 < endOfPrices2 * 1.035
        #
        # if not lessThan:
        #     print("Not less than")
        #     return 0

        # volumes3 = volumes.iloc[pivot: len(prices)]
        # std4 = volumes3.std()
        #
        # if std4 < 20:
        #     print("Failed due to STD: " + str(std4))
        #     return 0

        fluctuations = self._getNumberOfFluctuations(prices2)

        if fluctuations > 100:
            print("fluctuations > 100: " + str(fluctuations))
            return 0

        print("Fluctuations: " + str(fluctuations))
        print("Other STD: " + str(std2))
        return 1

    def _turnListOfFloatsToInputData(self, prices: List[float], volumes: List[float], numberOfSamples: int):
        if len(prices) + len(volumes) < numberOfSamples * 2:
            print("Not enough data was given to work with! (SimplePumpAndDumpDetector)")
            print("Data length: " + str(len(prices) + len(volumes)))
            return None, None

        return pd.Series(prices), pd.Series(volumes)

    def _setupDataForModel(self, prices, volumes):
        return prices, volumes

    def _getNumberOfFluctuations(self, series: pd.Series):
        series2 = series.diff()
        series2 = series2[series2 != 0]
        count = series2.size
        return count
