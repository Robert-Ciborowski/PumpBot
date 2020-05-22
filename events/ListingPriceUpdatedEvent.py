# Name: Listing Price Updated Event
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: An event which occurs when the price of a tracked listing has
#              been updated.

# from __future__ import annotations

from events.Event import Event

class ListingPriceUpdatedEvent(Event):
    def __init__(self, ticker: str):
        super().__init__("ListingPriceUpdated")
        self.data["Ticker"] = ticker
        print("Listing price updated: " + ticker)
