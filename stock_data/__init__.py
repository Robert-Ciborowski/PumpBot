from filter import StockFilterByPrice
from listing_obtainers import TSXObtainer
from stock_data.CurrentStockDataObtainer import CurrentStockDataObtainer
from stock_data.StockDatabase import StockDatabase
import time

if __name__ == "__main__":
    tsx_obtainer = TSXObtainer(20)
    filter = StockFilterByPrice(10)
    filter.addListings(tsx_obtainer)\
        .getPricesForListings()\
        .filterStocks()

    database = StockDatabase(3)
    database.useObtainer(CurrentStockDataObtainer())\
            .trackStocksInFilter(filter)\
            .startSelfUpdating()

    print("YO!")
    time.sleep(2)
    database.stopSelfUpdating()
    # print(database.getCurrentStock("AAB.TO"))

