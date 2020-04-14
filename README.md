# PumpBot
A machine learning stock market robot which detects and sends alerts about pump &amp; dump schemes on various stock markets. This program is meant to run on a server and send out alerts when it detects a pump &amp; dump.

## How it works
### Stocks
The program first downloads all listings from relevant markets (e.g. NASDAQ, TSX), usually via FTP. Afterwards, the program stores the listings that are penny stocks. Only penny stocks are stored because pump &amp; dump schemes typically occur with penny stocks, and not high-value stocks. The program keeps the prices of these listings up-to-date as it runs. Listing prices are obtained with the yfinance library.

### TensorFlow
We are using custom TensorFlow-powered classification neural networks to read the prices of these listings. The network outputs a single probability - the probability that the stock is beginning to experience a pump &amp; dump. The input layer accepts the most recent price changes of a penny stock. The output layer contains a single output node with our probability. The training data is custom-made.  We are willing to sacrifice some recall for higher precision. Note that this program uses TensorFlow 2.

### Discord
After a pump &amp; dump is detected, a Discord bot sends out an alert to a Discord server regarding the listing. The bot runs concurrently with the program. This bot uses Discord.py.

## Future plans
* Once we are confident with this bot's precision, we might add an auto-trade feature.
* We would also like to have our bot store its findings in a database. Then we can make a reactive web-app to view this database.
