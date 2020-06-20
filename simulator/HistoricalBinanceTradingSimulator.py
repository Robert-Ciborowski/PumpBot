import time
from datetime import datetime, timedelta

from events.EventDispatcher import EventDispatcher
from filter.PassThroughStockFilter import PassThroughStockFilter
from listing_obtainers.BinanceListingObtainer import BinanceListingObtainer
from listing_obtainers.SpecifiedListingObtainer import SpecifiedListingObtainer
from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
from stock_data.HistoricalBinanceDataObtainer import \
    HistoricalBinanceDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.BasicInvestmentStrategy import BasicInvestmentStrategy
from trading.MinutePumpTrader import MinutePumpTrader
from trading.ProfitPumpTrader import ProfitPumpTrader
from trading.PumpTrader import PumpTrader

from wallet.SimpleWallet import SimpleWallet
from wallet.Wallet import Wallet


class HistoricalBinanceTradingSimulator:
    startDate: datetime
    endDate: datetime
    maxTimeToHoldStock: int
    minutesAfterSellIfPump: int
    minutesAfterSellIfPriceInactivity: int
    minutesAfterSellIfLoss: int
    trader: PumpTrader
    database: TrackedStockDatabase
    dataObtainer: HistoricalBinanceDataObtainer
    model: CryptoPumpAndDumpDetector
    investmentFraction: float
    wallet: Wallet

    _fastForwardAmount: int

    def __init__(self, startDate: datetime, endDate: datetime, wallet: Wallet,
                 minutesBeforeSell: int, minutesAfterSell: int,
                 minutesAfterSellIfPriceInactivity: int,
                 minutesAfterSellIfLoss: int, investmentFraction: float,
                 fastForwardAmount=1):
        self.startDate = startDate
        self.endDate = endDate
        self.maxTimeToHoldStock = minutesBeforeSell
        self.minutesAfterSellIfPump = minutesAfterSell
        self.minutesAfterSellIfPriceInactivity = minutesAfterSellIfPriceInactivity
        self.minutesAfterSellIfLoss = minutesAfterSellIfLoss
        self._fastForwardAmount = fastForwardAmount
        self.investmentFraction = investmentFraction
        self.wallet = wallet
        self._setup()

    def _setup(self):
        # We add an hour to the end date just in case.
        self.dataObtainer = HistoricalBinanceDataObtainer(self.startDate,
                                                          self.endDate + timedelta(days=1),
                                                          filePathPrefix="../binance_historical_data/",
                                                          fastForwardAmount=self._fastForwardAmount)
        # tickers = ["BNBBTC", "BQXBTC", "FUNBTC", "GASBTC", "HSRBTC",
        #            "KNCBTC", "LRCBTC", "LTCBTC", "MCOBTC", "NEOBTC", "OAXBTC",
        #            "OMGBTC", "QTUMBTC", "SNGLSBTC", "STRATBTC", "WTCBTC",
        #            "YOYOBTC", "ZRXBTC"]
        # tickers = ["LRCBTC", "YOYOBTC"]
        # tickers = ["LRCBTC"]
        # tickers = ["OAXBTC"]
        tickers = ["LRCBTC", "YOYOBTC", "QTUMBTC", "FUNBTC", "LTCBTC", "SNGLSBTC"]
        # tickers = ["GASBTC", "KNCBTC", "STRATBTC", "MCOBTC", "NEOBTC", "ZRXBTC"]
        # listings_obtainer = SpecifiedListingObtainer(["OAXBTC"])
        listings_obtainer = SpecifiedListingObtainer(tickers)
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
        EventDispatcher.getInstance().addListener(self.model,
                                                  "ListingPriceUpdated")
        # self.trader = MinutePumpTrader(BasicInvestmentStrategy(self.investmentFraction),
        #                                Transactor(),
        #                                minutesBeforeSell=self.minutesBeforeSell,
        #                                minutesAfterSell=self.minutesAfterSell,
        #                                fastForwardAmount=self._fastForwardAmount,
        #                                startingFunds=self.startingFunds)
        self.trader = ProfitPumpTrader(
            BasicInvestmentStrategy(self.investmentFraction),
            self.wallet,
            profitRatioToAimFor=0.07,
            acceptableLossRatio=0.02,
            minutesAfterSellIfPump=self.minutesAfterSellIfPump,
            minutesAfterSellIfPriceInactivity=self.minutesAfterSellIfPriceInactivity,
            minutesAfterSellIfLoss=self.minutesAfterSellIfLoss,
            maxTimeToHoldStock=self.maxTimeToHoldStock,
            fastForwardAmount=self._fastForwardAmount)
        EventDispatcher.getInstance().addListener(self.trader, "PumpAndDump")

    def start(self):
        print("Starting historical Binance trading simulator...")
        self.database.startSelfUpdating()
        self.trader.start()
        self.dataObtainer.setStartTimeToNow()
        print("Started historical Binance trading simulator.")
        time.sleep((
                               self.endDate - self.startDate).total_seconds() // self._fastForwardAmount)
        print("It is time to stop.")
        self.database.stopSelfUpdating()
        self.trader.stop()
        print("Finished historical Binance trading simulation.")
        print("Results:")
        print(self.trader.tracker.tradesStr())
        print("=== Profits (in BTC) ===")
        print(self.trader.tracker.calculateProfits())
