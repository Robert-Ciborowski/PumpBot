from datetime import datetime

from simulator.HistoricalBinanceTradingSimulator import \
    HistoricalBinanceTradingSimulator

if __name__ == "__main__":
    start = datetime(2018, 8, 17, 15, 20)
    end = datetime(2018, 8, 17, 16, 15)
    simulator = HistoricalBinanceTradingSimulator(start, end, 7, 1.0, 0.3,
                                                  fastForwardAmount=10)
    simulator.start()
