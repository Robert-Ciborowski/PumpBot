import time
from datetime import datetime

from events.EventDispatcher import EventDispatcher
from filter.PassThroughStockFilter import PassThroughStockFilter
from listing_obtainers.BinanceListingObtainer import BinanceListingObtainer
from listing_obtainers.SpecifiedListingObtainer import SpecifiedListingObtainer
from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
from stock_data.HistoricalBinanceDataObtainer import \
    HistoricalBinanceDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.MinutePumpTrader import MinutePumpTrader

class HistoricalBinanceTradingSimulator:
    startDate: datetime
    endDate: datetime
    minutesBeforeSell: int
    trader: MinutePumpTrader
    database: TrackedStockDatabase

    def __init__(self, startDate: datetime, endDate: datetime, minutesBeforeSell: int):
        self.startDate = startDate
        self.endDate = endDate
        self.minutesBeforeSell = minutesBeforeSell
        self._setup()

    def _setup(self):
        dataObtainer = HistoricalBinanceDataObtainer(self.startDate, self.endDate, filePathPrefix="../data_set/")
        listings_obtainer = SpecifiedListingObtainer(["OAXBTC", "YOYOBTC"])
        filter = PassThroughStockFilter(dataObtainer)
        filter.addListings(listings_obtainer) \
            .getDataForFiltering() \
            .filter()

        self.database = TrackedStockDatabase.getInstance()
        self.database.useObtainer(dataObtainer) \
            .trackStocksInFilter(filter) \
            .setSecondsBetweenStockUpdates(60)

        model = CryptoPumpAndDumpDetector()
        model.setupUsingDefaults()
        model.createModelUsingDefaults()
        model.exportPath = "../models/model_exports/cryptopumpanddumpdetector"
        model.loadWeights()
        EventDispatcher.getInstance().addListener(model, "ListingPriceUpdated")

        print("DATA -----")
        print(dataObtainer.data)

        self.trader = MinutePumpTrader(self.minutesBeforeSell)
        EventDispatcher.getInstance().addListener(self.trader, "PumpAndDump")

    def start(self):
        print("Starting historical Binance trading simulator...")
        self.database.startSelfUpdating()
        self.trader.start()
        time.sleep(190885)
        print("It is time to stop.")
        self.database.stopSelfUpdating()
        self.trader.stop()
        print("Finished historical Binance trading simulation.")
