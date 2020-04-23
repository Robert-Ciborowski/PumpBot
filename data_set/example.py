from data_set.BinanceDataSetCreator import BinanceDataSetCreator

if __name__ == "__main__":
    from filter.PassThroughStockFilter import PassThroughStockFilter
    from listing_obtainers.TestObtainer import TestObtainer
    from datetime import datetime
    from stock_data.HistoricalBinanceDataObtainer import \
        HistoricalBinanceDataObtainer

    historicalObtainer = HistoricalBinanceDataObtainer(
        datetime(day=17, month=8, year=2018, hour=0, minute=1), datetime(day=31, month=8, year=2018, hour=0, minute=1),
        "../binance_historical_data/")
    historicalObtainer.trackStocks(["OAXBTC", "EOSETH", "ICNETH"])
    dataSetCreator = BinanceDataSetCreator(historicalObtainer)
    # dataSetCreator.findPumpAndDumps("OAXBTC", 0, 40000, plot=True)
    pumps, rightBeforePumps = dataSetCreator.findPumpsForSymbols(["OAXBTC", "EOSETH", "ICNETH"], 850)
    dataSetCreator.createFinalPumpsDataSet(pumps, rightBeforePumps)
    print(rightBeforePumps[0].columns)
    dataSetCreator.exportPumpsToCSV("OAXBTC-EOSETH-ICNETH", rightBeforePumps)
