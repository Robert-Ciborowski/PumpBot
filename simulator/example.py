from datetime import datetime

from simulator.HistoricalBinanceTradingSimulator import \
    HistoricalBinanceTradingSimulator

if __name__ == "__main__":
    start = datetime(2019, 1, 1, 12, 0)
    end = datetime(2019, 1, 3, 12, 0)
    simulator = HistoricalBinanceTradingSimulator(start, end, 1, fastForwardAmount=90)
    simulator.start()
