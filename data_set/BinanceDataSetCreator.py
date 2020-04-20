# Name: BinanceDataSetCreator
# Author: Robert Ciborowski
# Date: 19/04/2020
# Description: Creates a data set for Binance Pump & Dumps.

from stock_data import HistoricalBinanceDataObtainer

class BinanceDataSetCreator:
    dataObtainer: HistoricalBinanceDataObtainer

    def __init__(self, dataObtainer: HistoricalBinanceDataObtainer):
        self.dataObtainer = dataObtainer
