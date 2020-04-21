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
        final_df = self._analyse_symbol(symbol, df, 3, 1.05, plot=True)

    # returns final dataframe
    def _analyse_symbol(self, symbol: str, df: pd.DataFrame, volumeThreshold,
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
        num_v_spikes = self._get_num_rows(vdf)

        pmask, pdf = self._find_price_spikes(df, priceThreshold, windowSize)
        num_p_spikes = self._get_num_rows(pdf)

        pdmask, pddf = self._find_price_dumps(df, windowSize)

        vdmask, vddf = self._find_volume_dumps(df, windowSize)

        # find coinciding price and volume spikes
        vp_combined_mask = (volumeMask) & (pmask)
        vp_combined_df = df[vp_combined_mask]
        num_vp_combined_rows = self._get_num_rows(vp_combined_df)

        # coinciding price and volume spikes for alleged P&D (more than 1x per given time removed)
        vp_combined_rm = self._rm_same_day_pumps(vp_combined_df)
        num_alleged = self._get_num_rows(vp_combined_rm)

        # find coniciding price and volume spikes with dumps afterwards
        ''' at some point should probably be renamed '''
        final_combined_mask = (volumeMask) & (pmask) & (pdmask)
        final_combined = df[final_combined_mask]
        final_combined_rm = self._rm_same_day_pumps(
            final_combined)  # remove indicators which occur on the same day
        num_final_combined = self._get_num_rows(final_combined_rm)

        # -- plot --
        if plot is True:
            self._plot_pumps(symbol, exchangeName, windowSize, df, pdf, vdf,
                             vp_combined_df, pddf, final_combined, final_combined_rm,
                             plot_pRA=True, plot_ppeaks=True, plot_vRA=True,
                             plot_vpeaks=True)

        row_entry = {'Exchange': exchangeName,
                     'Symbol': symbol,
                     'Price Spikes': num_p_spikes,
                     'Volume Spikes': num_v_spikes,
                     'Alleged Pump and Dumps': num_alleged,
                     'Pump and Dumps': num_final_combined}

        return row_entry

    def _get_num_rows(self, df):
        return df.shape[0]

    def _rm_same_day_pumps(self, df):
        # Removes spikes that occur on the same day
        df = df.copy()
        df['Timestamp_DAYS'] = df['Timestamp'].apply(
            lambda x: x.replace(hour=0, minute=0, second=0))
        df = df.drop_duplicates(subset='Timestamp_DAYS', keep='last')
        return df

    # finds volume spikes in a given df, with a certain threshold and window size
    # returns a (boolean_mask,dataframe) tuple
    def _findVolumeSpikes(self, df, v_thresh, win_size):
        # -- add rolling average column to df --
        vRA = str(win_size) + 'h Volume RA'
        self._add_RA(df, win_size, 'Volume', vRA)

        # -- find spikes --
        vol_threshold = v_thresh * df[vRA]  # v_thresh increase in volume
        vol_spike_mask = df[
                             "Volume"] > vol_threshold  # where the volume is at least v_thresh greater than the x-hr RA
        df_vol_spike = df[vol_spike_mask]

        return (vol_spike_mask, df_vol_spike)

    # finds price spikes in a given df, with a certain threshold and window size
    # returns a (boolean_mask,dataframe) tuple
    def _find_price_spikes(self, df, p_thresh, win_size):
        # -- add rolling average column to df --
        pRA = str(win_size) + 'h Close Price RA'
        self._add_RA(df, win_size, 'Close', pRA)

        # -- find spikes --
        p_threshold = p_thresh * df[pRA]  # p_thresh increase in price
        p_spike_mask = df[
                           "High"] > p_threshold  # where the high is at least p_thresh greater than the x-hr RA
        df_price_spike = df[p_spike_mask]
        return (p_spike_mask, df_price_spike)

    # finds price dumps in a given df, with a certain threshold and window size
    # requires a price rolling average column of the proper window size and naming convention
    # returns a (boolean_mask,dataframe) tuple
    def _find_price_dumps(self, df, win_size):
        pRA = str(win_size) + "h Close Price RA"
        pRA_plus = pRA + "+" + str(win_size)

        df[pRA_plus] = df[pRA].shift(-win_size)
        price_dump_mask = df[pRA_plus] <= (df[pRA] + df[pRA].std())
        # if the xhour RA from after the pump was detected is <= the xhour RA (+std dev) from before the pump was detected
        # if the price goes from the high to within a range of what it was before

        df_p_dumps = df[price_dump_mask]
        return (price_dump_mask, df_p_dumps)

    def _find_volume_dumps(self, df, win_size):
        vRA = str(win_size) + "h Volume RA"
        vRA_plus = vRA + "+" + str(win_size)

        df[vRA_plus] = df[vRA].shift(-win_size)
        price_dump_mask = df[vRA_plus] <= (df[vRA] + df[vRA].std())
        # if the xhour RA from after the pump was detected is <= the xhour RA (+std dev) from before the pump was detected
        # if the volume goes from the high to within a range of what it was before

        df_p_dumps = df[price_dump_mask]
        return (price_dump_mask, df_p_dumps)

    # adds a rolling average column with specified window size to a given df and col
    def _add_RA(self, df, win_size, col, name):
        df[name] = pd.Series.rolling(df[col], window=win_size,
                                     center=False).mean()

    def _plot_markers(self, plot, df, xcol_name, ycol_name, color="red", marker="x",legend_name=None):
        markers = plot.scatter(df[xcol_name], df[ycol_name], color=color, marker=marker, legend=legend_name,
                               muted_alpha = 0.5, muted_color=color)
        markers.glyph.size = 10
        markers.glyph.line_width = 2
        markers.level = 'overlay'
        return markers

    def _plot_pumps(self, symbol_name,exchange_name,win_size,df,p_spike_df,v_spike_df,vp_combined_df,price_dump_df,final_df,final_df_rm,
                       plot_pRA=True,plot_ppeaks=True,plot_vRA=True,plot_vpeaks=True):
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

        p_candle = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, plot_height=450,
                          title = symbol_name+" Candlestick"+" | Exchange: "+exchange_name, y_axis_label='Price')
        p_candle.xaxis.major_label_orientation = pi/4
        p_candle.grid.grid_line_alpha=0.3

        # turn off scientific notation for y axis
        yaxis = p_candle.select(dict(type=Axis, layout="left"))[0]
        yaxis.formatter.use_scientific = False

        # plot candles
        p_candle.segment(df.Timestamp, df.High, df.Timestamp, df.Low, color="black")
        p_candle.vbar(df.Timestamp[inc], w, df.Open[inc], df.Close[inc], fill_color="#40a075", line_color="black") # green
        p_candle.vbar(df.Timestamp[dec], w, df.Open[dec], df.Close[dec], fill_color="#F2583E", line_color="black") # red

        # marking peaks
        if plot_ppeaks:
            price_peaks = self._plot_markers(p_candle,p_spike_df,'Timestamp','High',legend_name='Price Increase',color="orange")
            combined_peaks = self._plot_markers(p_candle,vp_combined_df,'Timestamp','High',legend_name='Price + Volume Increase',color="brown")
            price_dumps = self._plot_markers(p_candle,final_df,'Timestamp','High',legend_name='Price + Volume Increase + Volume Decrease',color="red")
            final = self._plot_markers(p_candle,final_df_rm,'Timestamp','High',legend_name='Pump and Dump',color="blue",marker="diamond")

        # price rolling avg
        if plot_pRA:
            pRA = str(win_size)+"h Close Price RA"
            p_ra_leg = str(win_size)+"h Rolling Avg."
            p_candle.line(df.Timestamp, df[pRA], line_width=2, color="green",legend=p_ra_leg)


        # add mutable legend
        p_candle.legend.location = "top_right"
        p_candle.legend.click_policy= "mute"


        # ---VOLUME PLOT---
        # create a new plot with a title and axis labels
        p_vol = figure(tools=TOOLS, x_axis_label='Date', y_axis_label='Volume',
                       x_axis_type="datetime",x_range=p_candle.x_range, plot_width=1000, plot_height=200)

        vol_yaxis = p_vol.select(dict(type=Axis, layout="left"))[0]
        vol_yaxis.formatter.use_scientific = False

        # plot volume
        p_vol.line(df.Timestamp, df.Volume, line_width=2)

        # marking peaks
        if plot_vpeaks:
            vol_peaks = self._plot_markers(p_vol,v_spike_df,'Timestamp','Volume',legend_name='Volume Increase',color="purple")
            combined_vol_peaks = self._plot_markers(p_vol,vp_combined_df,'Timestamp','Volume',legend_name='Price + Volume Increase',color="magenta")
            combined_dump_vol = self._plot_markers(p_vol,final_df,'Timestamp','Volume',legend_name='Price + Volume Increase + Volume Decrease',color="red")

        # rolling avg
        if plot_vRA:
            vRA = str(win_size)+"h Volume RA"
            v_ra_leg = str(win_size)+"h Rolling Avg."
            p_vol.line(df.Timestamp, df[vRA], line_width=2, color="green",legend=v_ra_leg)

        # add mutable legend
        p_vol.legend.location = "top_right"
        p_vol.legend.click_policy= "mute"

        # change num ticks
        p_candle.xaxis[0].ticker.desired_num_ticks = 20
        p_vol.xaxis[0].ticker.desired_num_ticks = 20


        # ---COMBINED PLOT---
        p = gridplot([[p_candle],[p_vol]])

        # output_notebook()
        p_candle.output_backend = "svg"
        p_vol.output_backend = "svg"
        show(p)
