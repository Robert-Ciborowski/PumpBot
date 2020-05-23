from typing import Dict, List

from trading.PumpTrade import PumpTrade


class PumpTradeTracker:
    trades: List

    def __init__(self):
        self.trades = []

    def addNewTrade(self, trade: PumpTrade):
        self.trades.append(trade)

    def containsUnsoldTrade(self, ticker: str) -> bool:
        for trade in self.trades:
            if trade.ticker == ticker and not trade.wasSold():
                return True

        return False

    def getTradeByTicker(self, ticker: str) -> PumpTrade:
        for trade in self.trades:
            if trade.ticker == ticker:
                return trade

        return None

    def calculateProfits(self) -> Dict:
        """
        Note: if a trade was not sold, the trade is marked as having a value of
        0!
        """
        returnDict = {}

        for trade in self.trades:
            if trade.wasSold():
                profit = 0.0
            else:
                profit = trade.sellPrice - trade.buyPrice

            if trade.ticker not in returnDict:
                returnDict[trade.ticker] = 0.0

            returnDict[trade.ticker] += profit

        return returnDict
