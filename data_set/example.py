from data_set.BinanceDataSetCreator import BinanceDataSetCreator

if __name__ == "__main__":
    from filter.PassThroughStockFilter import PassThroughStockFilter
    from listing_obtainers.TestObtainer import TestObtainer
    from datetime import datetime
    from stock_data.HistoricalBinanceDataObtainer import \
        HistoricalBinanceDataObtainer

    historicalObtainer = HistoricalBinanceDataObtainer(
        datetime(day=14, month=7, year=2017, hour=4, minute=0), datetime(day=14, month=7, year=2017, hour=4, minute=21),
        "../binance_historical_data/")
    historicalObtainer.trackStocks(["OAXBTC"])
    dataSetCreator = BinanceDataSetCreator(historicalObtainer)
    dataSetCreator.findPumpAndDumps("OAXBTC")
