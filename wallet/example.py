from wallet.BinanceWallet import BinanceWallet

if __name__ == "__main__":
    wallet = BinanceWallet()
    wallet.useBinanceKeysFromFile("../binance_properties.json")
    print(wallet.getBalanceDetailed("BTC"))
    print(wallet.purchase("OAXBTC", 30, test=True))
    print(wallet.sell("OAXBTC", 29, test=True))
    print(wallet.getDepositAddress())
    print(wallet.getWithdrawals())
    print(wallet.getTradeFee("OAXBTC"))
