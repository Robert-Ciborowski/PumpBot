# Name: TestObtainer
# Author: Robert Ciborowski
# Date: 12/04/2020
# Description: Generates a few listings.

# from __future__ import annotations

import pandas as pd
import urllib.request, json

from listing_obtainers.ListingObtainer import ListingObtainer

class TestObtainer(ListingObtainer):
    def __init__(self):
        super().__init__()

    def obtain(self) -> pd.DataFrame:
        dictionary = {
            "Ticker": ["BA", "AAPL"]
        }

        self.listings = pd.DataFrame(dictionary,
                                            columns=["Ticker", "Price"])

        return self.listings
