from datetime import datetime

from simulator.HistoricalBinanceTradingSimulator import \
    HistoricalBinanceTradingSimulator
from util.Constants import SAMPLES_OF_DATA_TO_LOOK_AT
from wallet.BinanceWallet import BinanceWallet
from wallet.SimpleWallet import SimpleWallet

if __name__ == "__main__":
    # LRCBTC, YOYOBTC, FUNBTC, GASBTC, KNCBTC, STRATBTC
    tickers = ["LRCBTC", "YOYOBTC", "FUNBTC", "GASBTC", "KNCBTC", "STRATBTC"]
    start = datetime(2020, 1, 17, 0, 0)
    end = datetime(2020, 1, 18, 0, 0)
    wallet = SimpleWallet(1.0)
    simulator = HistoricalBinanceTradingSimulator(start, end, wallet, 240, 120,
                                                  10, 40, 0.3, tickers, 5,
                                                  fastForwardAmount=4)
    simulator.start()
