# Name: Pump and Dump Model
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A super class for models that detect pump and dumps.

from __future__ import annotations

from typing import List

"""
Representation invariants:
- _decisionThreshold: is between 0 and 1, inclusive.
"""
class PumpAndDumpDetector:
    # Protected:
    _decisionThreshold: float

    def __init__(self, decisionThreshold: float):
        self.setDecisionThreshold(decisionThreshold)

    def detect(self, prices: List[int]) -> bool:
        print("Please use an implementation of PumpAndDumpDetector!")
        return False

    def setDecisionThreshold(self, decisionThreshold: float):
        self._decisionThreshold = decisionThreshold
