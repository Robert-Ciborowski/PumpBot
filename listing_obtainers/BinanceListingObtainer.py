# Name: BinanceListingObtainer
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Gets listings for Binance crypto.

# from __future__ import annotations

import pandas as pd

from listing_obtainers.ListingObtainer import ListingObtainer
import json
from binance.client import Client

class BinanceListingObtainer(ListingObtainer):
    _client: Client

    def __init__(self, propertiesFile="binance_properties.json"):
        super().__init__()
        api_key, api_secret = self._getKeysFromFile(propertiesFile)
        self._client = Client(api_key=api_key, api_secret=api_secret)

    def obtain(self) -> pd.DataFrame:
        dictionary = {
            "Ticker": []
        }

        tickers = self._client.get_all_tickers()

        for ticker in tickers:
            dictionary["Ticker"].append(ticker["symbol"])

        self.listings = pd.DataFrame(dictionary, columns=["Ticker"])

        return self.listings

    def _getKeysFromFile(self, propertiesFile: str):
        try:
            with open(propertiesFile, mode='r') as file:
                data = json.load(file)
                apiKey = data["API Key"]
                apiKeySecret = data["API Key Secret"]
                return apiKey, apiKeySecret
        except:
            print(
                "You are missing " + propertiesFile + ". Please ask Robert" \
                                                      "(robert.ciborowski"
                                                      "@mail.utoronto.ca) for "
                                                      "help.")
