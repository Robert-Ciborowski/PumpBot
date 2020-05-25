from datetime import datetime

from simulator.HistoricalBinanceTradingSimulator import \
    HistoricalBinanceTradingSimulator

if __name__ == "__main__":
    start = datetime(2018, 8, 17, 13, 30)
    end = datetime(2018, 8, 17, 16, 30)
    simulator = HistoricalBinanceTradingSimulator(start, end, 1, fastForwardAmount=60)
    simulator.start()
