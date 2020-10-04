# Name: Pump and Dump Model
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A super class for models that detect pump and dumps.

# from __future__ import annotations
from datetime import datetime, timedelta
from typing import Dict, List

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
    _lastUpdateTime: datetime

    def __init__(self):
        self._classificationThreshold = 0.0
        self._lastUpdateTime = datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0)

    def setClassificationThreshold(self, classificationThreshold: float):
        self._classificationThreshold = classificationThreshold
        # add stuff here?

    def detect(self, prices, volumes) -> bool:
        print("Please use an implementation of PumpAndDumpDetector!")
        return False

    def setClassificationThreshold(self, classificationThreshold: float):
        self._classificationThreshold = classificationThreshold

    def onEvent(self, event: Event):
        if event.type == "ListingPriceUpdated":
            currentDate = TrackedStockDatabase.getInstance().obtainer.getCurrentDate()

            # BAD!!!
            if self._lastUpdateTime.minute == currentDate.minute and self._lastUpdateTime.hour == currentDate.hour:
                return

            self._lastUpdateTime = currentDate
            prices, volumes = TrackedStockDatabase.getInstance().getMinuteStockPricesAndVolumes(event.data["Ticker"])
            # prices = TrackedStockDatabase.getInstance().getRecentStockPrices(event.data["Ticker"])
            # volumes = TrackedStockDatabase.getInstance().getRecentStockVolumes(event.data["Ticker"])

            if prices is None or volumes is None or len(prices) == 0 or len(volumes) == 0 or prices[0] is None or len(volumes) is None:
                print("An urgent error occurred inside of Pump and Dump detector!")
                return

            probability = self.detect(prices, volumes)

            if probability >= self._classificationThreshold:
                # Note: most recent price is at the end.
                currentPrice = prices[-1]
                EventDispatcher.getInstance().dispatchEvent(PumpAndDumpEvent(event.data["Ticker"], currentPrice, probability))
