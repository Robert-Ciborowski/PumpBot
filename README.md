# PumpBot
A machine learning cryptocurrency robot which detects and sends alerts about pump &amp; dump schemes on cryptocurrency exchanges and stock markets. This program is meant to run on a server and send out alerts when it detects a pump &amp; dump. The program is built using Python 3.6. 
- [Web Version](https://pumpbot.netlify.app/)
- [PumpBot Back-End API Documentation](https://documenter.getpostman.com/view/10732808/SzfDy63J?version=latest)

## Inspiration
This project is meant to expand on research on cryptocurrency pump &amp; dumps, which is an emerging problem in the field of criminal science. Specifically, this project is a continuation of the research done by Josh Kamps and Bennett Kleinberg of University College London on cryptocurrency pump &amp; dumps. (Kamps, J; Kleinberg, B; (2018) To the moon: defining and detecting cryptocurrency pump-and-dumps. Crime Science, 7, Article 18.) Their article can be found [here](https://discovery.ucl.ac.uk/id/eprint/10069142/).

## How it works
### Cryptocurrency Data
We are using APIs specific to each cryptocurrency exchange we analyze in order to obtain price and volume data. For example, cryptocurrency listings on Binance are obtained with the Binance API. Using exchange-specific APIs allows us to obtain accurate, real-time, minute specific information on each coin. When the program starts, it downloads a list of all coins on the exhange and keeps them updated in a database.

### Stock Data
In addition to cryptocurrency, our program is also built to analyze stock market data. The program first downloads all listings from relevant markets (e.g. NASDAQ, TSX), usually via FTP. Afterwards, the program filters out the listings that are not penny stocks. Only penny stocks are stored because pump &amp; dump stock schemes typically occur with penny stocks, and not high-value stocks. As with cryptocurrency listings, the program keeps the prices of penny stock listings up-to-date as it runs. Currently, stock listing prices are obtained with the yfinance library.

### TensorFlow
We are using custom TensorFlow-powered classification neural networks to interpret the real-time data of listings. The network outputs a single probability - the probability that the stock is beginning to experience a pump &amp; dump. The input layer accepts the most recent price changes of a penny stock. The output layer contains a single output node with our probability. Our training data is custom-made.  We are willing to sacrifice some recall for higher precision. Note that this program uses TensorFlow 2, which currently supports up to Python 3.6 (as of April 20th, 2020).

### Discord
After a pump &amp; dump is detected, a Discord bot sends out an alert to a Discord server regarding the listing. The bot runs concurrently with the program and is optional. This bot uses Discord.py.

### Database
Pump &amp; dump alerts are sent to a database. This database is read by a website, which serves as our front-end.


## Development Team
- [Robert Ciborowski](https://github.com/Robert-Ciborowski) - Machine learning developer and data analytics
- [Derek Wang](https://github.com/Derek-Y-Wang) - Discord bot helper
- [James Tang](https://github.com/jamestang12) - Full stack developer
