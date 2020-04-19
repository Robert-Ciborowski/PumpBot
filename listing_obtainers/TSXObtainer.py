# Name: TSXObtainer
# Author: Robert Ciborowski
# Date: 12/04/2020
# Description: Obtains all listings from the Toronto Stock Exchange.

# from __future__ import annotations

import pandas as pd
import urllib.request, json

from listing_obtainers.ListingObtainer import ListingObtainer

class TSXObtainer(ListingObtainer):
    amount_to_obtain: int

    """
    If amount_to_obtain is negative, then all listings will be obtained.
    You can just not pass it in since it's optional.
    """

    def __init__(self, amount_to_obtain=-1):
        super().__init__()
        self.amount_to_obtain = amount_to_obtain

    def obtain(self) -> pd.DataFrame:
        self.listings = pd.DataFrame(self.template)

        with urllib.request.urlopen("https://www.tsx.com/json/company-directory/search/tsx/.*") as url:
            data = json.loads(url.read().decode())

            for i in range(len(data["results"])):
                if 0 < self.amount_to_obtain <= i:
                    break

                df2 = pd.DataFrame({"Ticker": [data["results"][i]["symbol"] + ".TO"]})
                self.listings = self.listings.append(df2, ignore_index=True)

        return self.listings
