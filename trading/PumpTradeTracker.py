from datetime import datetime
from typing import Dict, List

from trading.PumpTrade import PumpTrade
from wallet.Wallet import Wallet


class PumpTradeTracker:
    trades: List

    def __init__(self):
        self.trades = []

    def addNewTrade(self, trade: PumpTrade):
        self.trades.append(trade)

    def isOwned(self, trade: PumpTrade) -> bool:
        """
        Adds a trade only if the stock with the ticker is not currently owned.
        :param trade: the trade
        :return: if the trade was successfully tracked
        """
        if not self.containsUnsoldTrade(trade.ticker):
            return True

        return False

    def containsUnsoldTrade(self, ticker: str) -> bool:
        for trade in self.trades:
            if trade.ticker == ticker and not trade.wasSold():
                return True

        return False

    def getUnsoldTradeByTicker(self, ticker: str) -> PumpTrade:
        for trade in self.trades:
            if trade.ticker == ticker and not trade.wasSold():
                return trade

        return None

    def calculateProfits(self) -> Dict:
        """
        Note: if a trade was not sold, the trade is marked as having a value of
        0!
        """
        returnDict = {}
        total = 0.0

        for trade in self.trades:
            profit = trade.calculateProfit()
            total += profit

            if trade.ticker not in returnDict:
                returnDict[trade.ticker] = 0.0

            returnDict[trade.ticker] += profit

        returnDict["Total"] = total
        return returnDict

    def tradesStr(self):
        string = ""

        for trade in self.trades:
            string += str(trade)

        return string

    def getNumberOfUnprofitableTradesOnDay(self, ticker: str, day: datetime):
        date = day.date()
        count = 0

        for trade in self.trades:
            if trade.ticker == ticker and trade.buyTimestamp.date() == date:
                count += 1

        return count

    def tradesCSV(self):
        string = "ticker,buy,sell,profit\n"
        profit = 0.0

        for trade in self.trades:
            profit += trade.calculateProfit()
            string += trade.ticker + "," + str(trade.buyTimestamp)\
                      + "," + str(trade.sellTimestamp) + "," + str(profit) + "\n"

        return string
