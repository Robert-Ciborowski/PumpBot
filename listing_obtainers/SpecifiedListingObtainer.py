# Name: SpecifiedListingObtainer
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Gives back a set of specified listings.

# from __future__ import annotations
from typing import List

import pandas as pd

from listing_obtainers.ListingObtainer import ListingObtainer
import json

class SpecifiedListingObtainer(ListingObtainer):
    _listings: List

    def __init__(self, listings: List[str]):
        super().__init__()
        self._listings = listings

    def obtain(self) -> pd.DataFrame:
        dictionary = {
            "Ticker": self._listings
        }

        self.listings = pd.DataFrame(dictionary, columns=["Ticker"])
        return self.listings
