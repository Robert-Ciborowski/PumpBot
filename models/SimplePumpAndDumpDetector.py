# Name: Dummy Pump and Dump Model
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A dummy test class used for detecting whether a stock is a
#              pump and dump. Don't use this class for anything other than
#              testing! All it does is generate a random value as its
#              probability! (The probability of its output being true is
#              the decision threshold itself.)

# from __future__ import annotations
from datetime import datetime
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

    def detect(self, prices) -> float:
        if prices is None:
            return False

        if isinstance(prices, List) or isinstance(prices, np.ndarray):
            # The list better contain only floats...
            volumes, prices = self._turnListOfFloatsToInputData(prices, SimplePumpAndDumpDetector._NUMBER_OF_SAMPLES)

            if volumes is None or prices is None:
                return 0

            return self._detect(volumes, prices)
        else:
            print("SimplePumpAndDumpDetector detect() had its precondition "
                  "violated!")
            return False

    def _detect(self, volumes, prices) -> float:
        # volumeStd = volumes.std()
        #
        # if volumeStd >= 2.0e-08:
        #     return False

        time1 = datetime.now()
        pricesStd = prices.std()

        if pricesStd < self.priceStdThreshold:
            result = 1
        else:
            result = 0

        time2 = datetime.now()
        print(str(pricesStd) + " vs " + str(self.priceStdThreshold))
        print("Gave out a result of " + str(result) + ", took " + str(
            time2 - time1))
        return result

    def _turnListOfFloatsToInputData(self, data: List[float], numberOfSamples: int):
        if len(data) < numberOfSamples * 2:
            return None, None

        return pd.Series(data[0 : numberOfSamples]), pd.Series(data[numberOfSamples : numberOfSamples * 2])
