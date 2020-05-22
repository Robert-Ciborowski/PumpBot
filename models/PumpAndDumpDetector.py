# Name: Pump and Dump Model
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A super class for models that detect pump and dumps.

# from __future__ import annotations

from typing import List

from events.EventListener import EventListener
from events.Event import Event
from events.EventDispatcher import EventDispatcher
from events.PumpAndDumpEvent import PumpAndDumpEvent
from stock_data.TrackedStockDatabase import TrackedStockDatabase
import numpy as np

"""
Representation invariants:
- _decisionThreshold: is between 0 and 1, inclusive.
"""
class PumpAndDumpDetector(EventListener):
    # Protected:
    _classificationThreshold: float

    def __init__(self):
        self._classificationThreshold = 0.0

    def setClassificationThreshold(self, classificationThreshold: float):
        self._classificationThreshold = classificationThreshold
        # add stuff here?

    def detect(self, prices) -> bool:
        print("Please use an implementation of PumpAndDumpDetector!")
        return False

    def setClassificationThreshold(self, classificationThreshold: float):
        self._classificationThreshold = classificationThreshold

    def onEvent(self, event: Event):
        if event.type == "ListingPriceUpdated":
            prices = TrackedStockDatabase.getInstance().getRecentStockPrices(event.data["Ticker"])
            volumes = TrackedStockDatabase.getInstance().getRecentStockVolumes(event.data["Ticker"])
            currentPrice = prices[-1]
            prices, volumes = self._setupDataForModel(prices, volumes)
            probability = self.detect(volumes + prices)

            if probability >= self._classificationThreshold:
                # Note: most recent price is at the end.
                EventDispatcher.getInstance().dispatchEvent(PumpAndDumpEvent(event.data["Ticker"], currentPrice))

    def _setupDataForModel(self, prices, volumes):
        from scipy import stats
        prices = stats.zscore(prices)
        volumes = stats.zscore(volumes)
        prices = [np.array([x]) for x in prices]
        volumes = [np.array([x]) for x in volumes]
        return prices, volumes
