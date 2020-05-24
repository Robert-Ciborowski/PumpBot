# Name: TestListingObtainer
# Author: Robert Ciborowski
# Date: 12/04/2020
# Description: Generates a few listings.

# from __future__ import annotations

import pandas as pd
import urllib.request, json

from listing_obtainers.ListingObtainer import ListingObtainer

class TestListingObtainer(ListingObtainer):
    dummyTicker: str

    def __init__(self, dummyTicker="AAPL"):
        super().__init__()
        self.dummyTicker = dummyTicker

    def obtain(self) -> pd.DataFrame:
        dictionary = {
            "Ticker": [self.dummyTicker],
            "Price": [0]
        }

        self.listings = pd.DataFrame(dictionary,
                                            columns=["Ticker", "Price"])

        return self.listings
