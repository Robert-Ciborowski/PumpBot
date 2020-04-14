# Name: Dummy Pump and Dump Model
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A dummy test class used for detecting whether a stock is a
#              pump and dump. Don't use this class for anything other than
#              testing! All it does is generate a random value as its
#              probability! (The probability of its output being true is
#              the decision threshold itself.)

from __future__ import annotations
from typing import List
import random

from models.PumpAndDumpModel import PumpAndDumpDetector

class DummyPumpAndDumpDetector(PumpAndDumpDetector):
    def detect(self, prices: List[int]) -> bool:
        return random.random() <= self._classificationThreshold
