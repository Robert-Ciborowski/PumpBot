# Name: BinanceDataSetCreator
# Author: Robert Ciborowski
# Date: 19/04/2020
# Description: Creates a data set for Binance Pump & Dumps.
from math import pi

from stock_data import HistoricalBinanceDataObtainer
import pandas as pd
from datetime import datetime
#plotting
from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svgs
from bokeh.io import output_notebook
from bokeh.models import Axis, ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.plotting import figure

class BinanceDataSetCreator:
    dataObtainer: HistoricalBinanceDataObtainer

    def __init__(self, dataObtainer: HistoricalBinanceDataObtainer):
        self.dataObtainer = dataObtainer

    def findPumpAndDumps(self, symbol: str):
        """
        NOTE: FOR NOW, let's just try and make this function with the help of
        that research paper.
        :param df:
        :return:
        """
        df = self.dataObtainer._data[symbol]
        final_df = self._analyseSymbol(symbol, df, 3, 1.05, plot=True)

    # returns final dataframe
    def _analyseSymbol(self, symbol: str, df: pd.DataFrame, volumeThreshold,
                       priceThreshold, windowSize=24, candleSize='1m',
                       plot=False):
        '''
        USAGE:
        f_path : path to OHLCV csv e.g.'../data/binance/binance_STORJ-BTC_[2018-04-20 00.00.00]-TO-[2018-05-09 23.00.00].csv'
        v_thresh : volume threshold e.g. 5 (500%)
        p_thresh : price threshold e.g. 1.05 (5%)
        c_size : candle size
        win_size : size of the window for the rolling average, in hours
        '''
        exchangeName = "binance"

        # This finds spikes for volume and price.
        volumeMask, vdf = self._findVolumeSpikes(df, volumeThreshold, windowSize)
        volumeSpikeAmount = self._getNumberOfRows(vdf)

        pmask, pdf = self._findPriceSpikes(df, priceThreshold, windowSize)
        priceSpikeAmount = self._getNumberOfRows(pdf)

        pdmask, pddf = self._findPriceDumps(df, windowSize)

        vdmask, vddf = self._findVolumeDumps(df, windowSize)

        # find coinciding price and volume spikes
        volumePriceMask = (volumeMask) & (pmask)
        volumePriceDF = df[volumePriceMask]
        volumePriceCombinedRowsAmount = self._getNumberOfRows(volumePriceDF)

        # coinciding price and volume spikes for alleged P&D (more than 1x per given time removed)
        volumePriceFinalDF = self._removeSameDayPumps(volumePriceDF)
        allegedAmount = self._getNumberOfRows(volumePriceFinalDF)

        # find coniciding price and volume spikes with dumps afterwards
        ''' at some point should probably be renamed '''
        finalMask = (volumeMask) & (pmask) & (pdmask)
        finalDF = df[finalMask]

        #  remove indicators which occur on the same day
        finalCombined = self._removeSameDayPumps(finalDF)
        finalCombinedAmount = self._getNumberOfRows(finalCombined)

        # -- plot --
        if plot is True:
            self._plotPumps(symbol, exchangeName, windowSize, df, pdf, vdf,
                            volumePriceDF, pddf, finalDF, finalCombined,
                            plotPriceRA=True, plotPricePeaks=True, plotVolumeRA=True,
                            plotVolumePeaks=True)

        rowEntry = {'Exchange': exchangeName,
                     'Symbol': symbol,
                     'Price Spikes': priceSpikeAmount,
                     'Volume Spikes': volumeSpikeAmount,
                     'Alleged Pump and Dumps': allegedAmount,
                     'Pump and Dumps': finalCombinedAmount}

        return rowEntry

    def _getNumberOfRows(self, df):
        return df.shape[0]

    def _removeSameDayPumps(self, df):
        # Removes spikes that occur on the same day
        df = df.copy()
        df['Timestamp_DAYS'] = df['Timestamp'].apply(
            lambda x: x.replace(hour=0, minute=0, second=0))
        df = df.drop_duplicates(subset='Timestamp_DAYS', keep='last')
        return df

    # finds volume spikes in a given df, with a certain threshold and window size
    # returns a (boolean_mask,dataframe) tuple
    def _findVolumeSpikes(self, df, volumeThreshold, windowSize):
        # -- add rolling average column to df --
        vRA = str(windowSize) + 'h Volume RA'
        self._addRA(df, windowSize, 'Volume', vRA)

        # -- find spikes --
        volumeThreshold = volumeThreshold * df[vRA]  # v_thresh increase in volume
        volumeSpikeMask = df["Volume"] > volumeThreshold  # where the volume is at least v_thresh greater than the x-hr RA
        volumeSpikeDF = df[volumeSpikeMask]
        return (volumeSpikeMask, volumeSpikeDF)

    # finds price spikes in a given df, with a certain threshold and window size
    # returns a (boolean_mask,dataframe) tuple
    def _findPriceSpikes(self, df, priceThreshold, windowSize):
        # -- add rolling average column to df --
        pRA = str(windowSize) + 'h Close Price RA'
        self._addRA(df, windowSize, 'Close', pRA)

        # -- find spikes --
        newThreshold = priceThreshold * df[pRA]  # p_thresh increase in price
        priceSpikeMask = df["High"] > newThreshold  # where the high is at least p_thresh greater than the x-hr RA
        priceSpikeDF = df[priceSpikeMask]
        return (priceSpikeMask, priceSpikeDF)

    # finds price dumps in a given df, with a certain threshold and window size
    # requires a price rolling average column of the proper window size and naming convention
    # returns a (boolean_mask,dataframe) tuple
    def _findPriceDumps(self, df, windowSize):
        pRA = str(windowSize) + "h Close Price RA"
        pRA_plus = pRA + "+" + str(windowSize)

        df[pRA_plus] = df[pRA].shift(-windowSize)
        priceDumpMask = df[pRA_plus] <= (df[pRA] + df[pRA].std())
        # if the xhour RA from after the pump was detected is <= the xhour RA (+std dev) from before the pump was detected
        # if the price goes from the high to within a range of what it was before

        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _findVolumeDumps(self, df, windowSize):
        vRA = str(windowSize) + "h Volume RA"
        vRA_plus = vRA + "+" + str(windowSize)

        df[vRA_plus] = df[vRA].shift(-windowSize)
        priceDumpMask = df[vRA_plus] <= (df[vRA] + df[vRA].std())
        # if the xhour RA from after the pump was detected is <= the xhour RA (+std dev) from before the pump was detected
        # if the volume goes from the high to within a range of what it was before

        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    # adds a rolling average column with specified window size to a given df and col
    def _addRA(self, df, windowSize, col, name):
        df[name] = pd.Series.rolling(df[col], window=windowSize,
                                     center=False).mean()

    def _plotMarkers(self, plot, df, xColumnName, yColumnName, color="red", marker="x", legendName=None):
        markers = plot.scatter(df[xColumnName], df[yColumnName], color=color, marker=marker, legend=legendName,
                               muted_alpha=0.5, muted_color=color)
        markers.glyph.size = 10
        markers.glyph.line_width = 2
        markers.level = 'overlay'
        return markers

    def _plotPumps(self, symbolName, exchangeName, winSize, df, priceSpikeDF, volumeSpikeDF, volumePriceCombinedDF, price_dump_df, final_df, final_df_rm,
                   plotPriceRA=True, plotPricePeaks=True, plotVolumeRA=True, plotVolumePeaks=True):
        '''
        Still needs support for different candle times (change w, not hard)
        '''
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

        # ---CANDLE PLOT---
        inc = df.Close > df.Open
        dec = df.Open > df.Close

        msec = 1000
        minute = 60 * msec
        hour = 60 * minute

        w = hour/2 # half an hour (should be half the candle size)

        priceCandle = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, plot_height=450,
                          title =symbolName + " Candlestick" + " | Exchange: " + exchangeName, y_axis_label='Price')
        priceCandle.xaxis.major_label_orientation = pi/4
        priceCandle.grid.grid_line_alpha=0.3

        # turn off scientific notation for y axis
        yaxis = priceCandle.select(dict(type=Axis, layout="left"))[0]
        yaxis.formatter.use_scientific = False

        # plot candles
        priceCandle.segment(df.Timestamp, df.High, df.Timestamp, df.Low, color="black")
        priceCandle.vbar(df.Timestamp[inc], w, df.Open[inc], df.Close[inc], fill_color="#40a075", line_color="black") # green
        priceCandle.vbar(df.Timestamp[dec], w, df.Open[dec], df.Close[dec], fill_color="#F2583E", line_color="black") # red

        # marking peaks
        if plotPricePeaks:
            price_peaks = self._plotMarkers(priceCandle, priceSpikeDF, 'Timestamp', 'High', legendName='Price Increase', color="orange")
            combined_peaks = self._plotMarkers(priceCandle, volumePriceCombinedDF, 'Timestamp', 'High', legendName='Price + Volume Increase', color="brown")
            price_dumps = self._plotMarkers(priceCandle, final_df, 'Timestamp', 'High', legendName='Price + Volume Increase + Volume Decrease', color="red")
            final = self._plotMarkers(priceCandle, final_df_rm, 'Timestamp', 'High', legendName='Pump and Dump', color="blue", marker="diamond")

        # price rolling avg
        if plotPriceRA:
            pRA = str(winSize) + "h Close Price RA"
            legend = str(winSize) + "h Rolling Avg."
            priceCandle.line(df.Timestamp, df[pRA], line_width=2, color="green",legend=legend)


        # add mutable legend
        priceCandle.legend.location = "top_right"
        priceCandle.legend.click_policy= "mute"


        # ---VOLUME PLOT---
        # create a new plot with a title and axis labels
        priceVolume = figure(tools=TOOLS, x_axis_label='Date', y_axis_label='Volume',
                       x_axis_type="datetime",x_range=priceCandle.x_range, plot_width=1000, plot_height=200)

        vol_yaxis = priceVolume.select(dict(type=Axis, layout="left"))[0]
        vol_yaxis.formatter.use_scientific = False

        # plot volume
        priceVolume.line(df.Timestamp, df.Volume, line_width=2)

        # marking peaks
        if plotVolumePeaks:
            vol_peaks = self._plotMarkers(priceVolume, volumeSpikeDF, 'Timestamp', 'Volume', legendName='Volume Increase', color="purple")
            combined_vol_peaks = self._plotMarkers(priceVolume, volumePriceCombinedDF, 'Timestamp', 'Volume', legendName='Price + Volume Increase', color="magenta")
            combined_dump_vol = self._plotMarkers(priceVolume, final_df, 'Timestamp', 'Volume', legendName='Price + Volume Increase + Volume Decrease', color="red")

        # rolling avg
        if plotVolumeRA:
            vRA = str(winSize) + "h Volume RA"
            v_ra_leg = str(winSize) + "h Rolling Avg."
            priceVolume.line(df.Timestamp, df[vRA], line_width=2, color="green",legend=v_ra_leg)

        # add mutable legend
        priceVolume.legend.location = "top_right"
        priceVolume.legend.click_policy= "mute"

        # change num ticks
        priceCandle.xaxis[0].ticker.desired_num_ticks = 20
        priceVolume.xaxis[0].ticker.desired_num_ticks = 20


        # ---COMBINED PLOT---
        p = gridplot([[priceCandle],[priceVolume]])

        # output_notebook()
        priceCandle.output_backend = "svg"
        priceVolume.output_backend = "svg"
        show(p)
