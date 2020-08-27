import time
from datetime import datetime, timedelta
from typing import List
import pandas as pd
import numpy as np
import threading as th

from events.EventDispatcher import EventDispatcher
from filter.PassThroughStockFilter import PassThroughStockFilter
from listing_obtainers.BinanceListingObtainer import BinanceListingObtainer
from listing_obtainers.SpecifiedListingObtainer import SpecifiedListingObtainer
from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
from models.SimplePumpAndDumpDetector import SimplePumpAndDumpDetector
from stock_data.HistoricalBinanceDataObtainer import \
    HistoricalBinanceDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from thread_runner.ThreadRunner import ThreadRunner
from trading.BasicInvestmentStrategy import BasicInvestmentStrategy
from trading.MinutePumpTrader import MinutePumpTrader
from trading.ProfitPumpTrader import ProfitPumpTrader
from trading.PumpTrader import PumpTrader
from wallet.SimpleWallet import SimpleWallet
from wallet.Wallet import Wallet
from logger.Logger import Logger


class HistoricalBinanceTradingSimulator:
    startDate: datetime
    endDate: datetime
    maxTimeToHoldStock: int
    minutesAfterSellIfPump: int
    minutesAfterSellIfPriceInactivity: int
    minutesAfterSellIfLoss: int
    unprofitableTradesPerDay: int
    trader: PumpTrader
    database: TrackedStockDatabase
    dataObtainer: HistoricalBinanceDataObtainer
    model: CryptoPumpAndDumpDetector
    investmentFraction: float
    wallet: Wallet
    tickers: List
    modelLocation: str
    historicalDataLocation: str
    threadRunner: ThreadRunner

    _fastForwardAmount: int

    def __init__(self, startDate: datetime, endDate: datetime, wallet: Wallet,
                 minutesBeforeSell: int, minutesAfterSell: int,
                 minutesAfterSellIfPriceInactivity: int,
                 minutesAfterSellIfLoss: int, investmentFraction: float,
                 coins: List, unprofitableTradesPerDay: int, fastForwardAmount=1,
                 modelLocation="../models/model_exports/cryptopumpanddumpdetector",
                 historicalDataLocation="../binance_historical_data"):
        self.startDate = startDate
        self.endDate = endDate
        self.maxTimeToHoldStock = minutesBeforeSell
        self.minutesAfterSellIfPump = minutesAfterSell
        self.minutesAfterSellIfPriceInactivity = minutesAfterSellIfPriceInactivity
        self.minutesAfterSellIfLoss = minutesAfterSellIfLoss
        self._fastForwardAmount = fastForwardAmount
        self.investmentFraction = investmentFraction
        self.unprofitableTradesPerDay = unprofitableTradesPerDay
        self.wallet = wallet
        self.tickers = coins
        self.modelLocation = modelLocation
        self.historicalDataLocation = historicalDataLocation
        self.threadRunner = ThreadRunner()
        self._setup()

    def _setup(self):
        import sys
        sys.stdout = Logger("simulator_output.txt")

        # We add an hour to the end date just in case.
        self.dataObtainer = HistoricalBinanceDataObtainer(self.startDate,
                                                          self.endDate + timedelta(days=1),
                                                          filePathPrefix=self.historicalDataLocation + "/",
                                                          fastForwardAmount=self._fastForwardAmount)
        listings_obtainer = SpecifiedListingObtainer(self.tickers)
        filter = PassThroughStockFilter(self.dataObtainer)
        filter.addListings(listings_obtainer) \
            .getDataForFiltering() \
            .filter()

        self.database = TrackedStockDatabase.getInstance()
        self.database.useObtainer(self.dataObtainer) \
            .trackStocksInFilter(filter) \
            .setSecondsBetweenStockUpdates(60 / self._fastForwardAmount)
        # .setSecondsBetweenStockUpdates(60)

        # self.model = CryptoPumpAndDumpDetector(tryUsingGPU=False)
        # self.model.setupUsingDefaults()
        # self.model.createModelUsingDefaults()
        # self.model.exportPath = self.modelLocation
        # self.model.loadWeights()
        # self.model.prepareForUse()
        # 2.0e-08
        self.model = SimplePumpAndDumpDetector(2.0e-08, 2.0e-08)
        EventDispatcher.getInstance().addListener(self.model,
                                                  "ListingPriceUpdated")
        self.database.model = self.model


        # self.trader = MinutePumpTrader(BasicInvestmentStrategy(self.investmentFraction),
        #                                Transactor(),
        #                                minutesBeforeSell=self.minutesBeforeSell,
        #                                minutesAfterSell=self.minutesAfterSell,
        #                                fastForwardAmount=self._fastForwardAmount,
        #                                startingFunds=self.startingFunds)
        print("MAIN THREAD: " + str(th.current_thread().ident))
        self.trader = ProfitPumpTrader(
            BasicInvestmentStrategy(self.investmentFraction),
            self.wallet,
            # profitRatioToAimFor=0.05,
            profitRatioToAimFor=0.04,
            acceptableLossRatio=0.03,
            acceptableDipFromStartRatio=0.02,
            minutesAfterSellIfPump=self.minutesAfterSellIfPump,
            minutesAfterSellIfPriceInactivity=self.minutesAfterSellIfPriceInactivity,
            minutesAfterSellIfLoss=self.minutesAfterSellIfLoss,
            maxTimeToHoldStock=self.maxTimeToHoldStock,
            unprofitableTradesPerDay=self.unprofitableTradesPerDay,
            fastForwardAmount=self._fastForwardAmount)
        EventDispatcher.getInstance().addListener(self.trader, "PumpAndDump")

    def start(self):
        print("Starting historical Binance trading simulator...")

        # If not using threadrunner:
        # self.database.startSelfUpdating()
        # self.trader.start()

        # If using threadrunner:
        self.database.useThreadRunner(self.threadRunner)
        self.trader.useThreadRunner(self.threadRunner)
        sleepAmount = (self.endDate - self.startDate).total_seconds() // self._fastForwardAmount
        self.threadRunner.endTime = datetime.now() + timedelta(seconds=sleepAmount)

        self.dataObtainer.setStartTimeToNow()

        print("Started historical Binance trading simulator.")
        self.threadRunner.start()

        print("It is time to stop.")
        # self.database.stopSelfUpdating()
        # self.trader.stop()
        print("Finished historical Binance trading simulation.")

        trades = self.trader.tracker.tradesStr()
        tradesAsCSV = self.trader.tracker.tradesCSV()
        profits = str(self.trader.tracker.calculateProfits())

        print("Results:")
        print(trades)
        print("=== Profits (in BTC) ===")
        print(profits)

        f = open("simulator_trades.txt", "w")
        f.write(trades)
        f.write("\n")
        f.write(profits)
        f.close()

        f = open("simulator_trades.csv", "w")
        f.write(tradesAsCSV)
        f.close()
