from datetime import datetime

from simulator.HistoricalBinanceTradingSimulator import \
    HistoricalBinanceTradingSimulator

if __name__ == "__main__":
    start = datetime(2018, 8, 17, 15, 20)
    end = datetime(2018, 8, 17, 16, 15)
    simulator = HistoricalBinanceTradingSimulator(start, end, 1, 1.0, 0.07,
                                                  fastForwardAmount=5)
    simulator.start()
