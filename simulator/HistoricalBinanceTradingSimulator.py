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
    _fastForwardAmount: int
    trader: MinutePumpTrader
    database: TrackedStockDatabase
    dataObtainer: HistoricalBinanceDataObtainer
    model: CryptoPumpAndDumpDetector

    def __init__(self, startDate: datetime, endDate: datetime,
                 minutesBeforeSell: int, fastForwardAmount=1):
        self.startDate = startDate
        self.endDate = endDate
        self.minutesBeforeSell = minutesBeforeSell
        self._fastForwardAmount = fastForwardAmount
        self._setup()

    def _setup(self):
        self.dataObtainer = HistoricalBinanceDataObtainer(self.startDate, self.endDate,
                                                     filePathPrefix="../binance_historical_data/",
                                                     fastForwardAmount=self._fastForwardAmount)
        listings_obtainer = SpecifiedListingObtainer(["OAXBTC"])
        filter = PassThroughStockFilter(self.dataObtainer)
        filter.addListings(listings_obtainer) \
            .getDataForFiltering() \
            .filter()

        self.database = TrackedStockDatabase.getInstance()
        self.database.useObtainer(self.dataObtainer) \
            .trackStocksInFilter(filter) \
            .setSecondsBetweenStockUpdates(60 / self._fastForwardAmount)
            # .setSecondsBetweenStockUpdates(60)

        self.model = CryptoPumpAndDumpDetector()
        self.model.setupUsingDefaults()
        self.model.createModelUsingDefaults()
        self.model.exportPath = "../models/model_exports/cryptopumpanddumpdetector"
        self.model.loadWeights()
        self.model.prepareForUse()
        EventDispatcher.getInstance().addListener(self.model, "ListingPriceUpdated")
        self.trader = MinutePumpTrader(self.minutesBeforeSell, fastForwardAmount=self._fastForwardAmount)
        EventDispatcher.getInstance().addListener(self.trader, "PumpAndDump")

    def start(self):
        print("Starting historical Binance trading simulator...")
        self.database.startSelfUpdating()
        self.trader.start()
        self.dataObtainer.setStartTimeToNow()
        print("Started historical Binance trading simulator.")
        time.sleep((self.endDate - self.startDate).total_seconds() // self._fastForwardAmount)
        print("It is time to stop.")
        self.database.stopSelfUpdating()
        self.trader.stop()
        print("Finished historical Binance trading simulation.")
        print("Results:")
        print(self.trader.tracker.calculateProfits())
