from wallet.BinanceTransactor import BinanceTransactor

if __name__ == "__main__":
    transactor = BinanceTransactor()
    transactor.useBinanceKeysFromFile("../binance_properties.json")
    print(transactor.getBalanceDetailed("BTC"))
    print(transactor.purchase("OAXBTC", 30, test=True))
    print(transactor.sell("OAXBTC", 29, test=True))
