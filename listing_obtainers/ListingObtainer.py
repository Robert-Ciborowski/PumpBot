# Name: ListingObtainer
# Author: Robert Ciborowski
# Date: 12/04/2020
# Description: Obtains all listings from some market.

from __future__ import annotations

from typing import Dict
import pandas as pd

class ListingObtainer:
    template: Dict
    listings: pd.DataFrame

    def __init__(self):
        self.template = {
            "Ticker": []
        }

    def obtain(self) -> pd.DataFrame:
        self.listings = pd.DataFrame(self.template)
        return self.listings
