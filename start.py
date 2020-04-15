# Name: Start
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: Starts the program.
import time

from events import EventDispatcher
from example_bot import ExampleBot
from filter import StockFilterByPrice
from listing_obtainers.NASDAQObtainer import NASDAQObtainer
from models.DummyPumpAndDumpDetector import DummyPumpAndDumpDetector
from stock_data import StockDatabase, CurrentStockDataObtainer
from datetime import datetime

from stock_data.HistoricStockDataObtainer import HistoricStockDataObtainer

if __name__ == "__main__":
    # April 1st, 2020 at 11:30 am.
    stockDataObtainer = HistoricStockDataObtainer(datetime(2020, 4, 1, 11, 30))
    # stockDataObtainer = CurrentStockDataObtainer()
    nasdaq_obtainer = NASDAQObtainer(20)
    filter = StockFilterByPrice(10, stockDataObtainer)
    filter.addListings(nasdaq_obtainer)\
        .getPricesForListings()\
        .filterStocks()

    database = StockDatabase.getInstance()
    database.useObtainer(stockDataObtainer)\
           .trackStocksInFilter(filter)\
           .setSecondsBetweenStockUpdates(15)

    bot = ExampleBot()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    model = DummyPumpAndDumpDetector(0.5)
    EventDispatcher.getInstance().addListener(model, "ListingPriceUpdated")

    database.startSelfUpdating()

    time.sleep(75)
    database.stopSelfUpdating()
    # print(database.getCurrentStock("AAB.TO"))
