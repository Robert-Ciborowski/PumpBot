from datetime import datetime

from simulator.HistoricalBinanceTradingSimulator import \
    HistoricalBinanceTradingSimulator

if __name__ == "__main__":
    start = datetime(2019, 1, 1, 12)
    end = datetime(2019, 1, 2, 12)
    simulator = HistoricalBinanceTradingSimulator(start, end, 1)
    simulator.start()
