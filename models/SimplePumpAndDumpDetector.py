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
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT


class SimplePumpAndDumpDetector(PumpAndDumpDetector):
    _NUMBER_OF_SAMPLES = MINUTES_OF_DATA_TO_LOOK_AT
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

        pivot = int(len(prices) * 0.95)
        prices2 = prices.iloc[0 : pivot]
        std2 = prices2.std()

        if std2 > 2.0e-08:
            return 0

        prices3 = prices.iloc[pivot: len(prices)]
        std3 = prices3.std()

        if std3 > 7.0e-08:
            return 0

        greaterThan = prices3.iloc[-1] > prices2.iloc[-1] * 1.01
        lessThan = prices3.iloc[-1] < prices2.iloc[-1] * 1.025

        if greaterThan and lessThan:
            return 1

        return 0

    def _turnListOfFloatsToInputData(self, prices: List[float], volumes: List[float], numberOfSamples: int):
        if len(prices) + len(volumes) < numberOfSamples * 2:
            print("Not enough data was given to work with! (SimplePumpAndDumpDetector)")
            return None, None

        return pd.Series(prices), pd.Series(volumes)

    def _setupDataForModel(self, prices, volumes):
        return prices, volumes
