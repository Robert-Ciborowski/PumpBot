import pandas as pd
import math
import os.path
import time
# from bitmex import bitmex
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
# from tqdm import tqdm_notebook #(Optional, used for progress-bars)

### API
binance_api_key = ""    #Enter your own API-key here
binance_api_secret = "" #Enter your own API-secret here

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
# bitmex_client = bitmex(test=False, api_key=bitmex_api_key, api_secret=bitmex_api_secret)
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

# place a test market buy order, to place an actual order use the create_order function
# order = binance_client.create_test_order(
#     symbol='BNBBTC',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=100)
#
# print(order)

info = binance_client.get_symbol_info("OAXBTC")
stepSize = float(info["filters"][2]["stepSize"])
precision = int(round(-math.log(stepSize, 10), 0))
amountInSellCurrency = 0.001301331 / 0.00000390
# amountInSellCurrency = 0.003034031 / 0.00000390

order = binance_client.create_order(
    symbol='OAXBTC',
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity=round(amountInSellCurrency, precision))

print(order)

# get all symbol prices
prices = binance_client.get_all_tickers()
print(prices)

# withdraw 100 ETH
# check docs for assumptions around withdrawals
# from binance.exceptions import BinanceAPIException, BinanceWithdrawException
# try:
#     result = binance_client.withdraw(
#         asset='ETH',
#         address='<eth_address>',
#         amount=100)
# except BinanceAPIException as e:
#     print(e)
# except BinanceWithdrawException as e:
#     print(e)
# else:
#     print("Success")
#
# fetch list of withdrawals
withdraws = binance_client.get_withdraw_history()
print(withdraws)
#
# fetch list of withdrawals
eth_withdraws = binance_client.get_withdraw_history(asset='BTC')
print(eth_withdraws)
#
# # get a deposit address for BTC
# address = binance_client.get_deposit_address(asset='BTC')
# print(address)
