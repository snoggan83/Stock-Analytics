from matplotlib import pyplot as plt
from matplotlib.finance import candlestick_ohlc
import talib as ta
import Getdata
import Loaddata
import numpy as np
from datetime import datetime, date
import matplotlib.dates as dt

# Initializing Properties

# Stock tag
tag = 'LargeCap'
# tag = 'MidCap'
# tag = 'SmallCap'
# tag = 'Commodities'
# tag = 'Index'

#  Running mode
mode = 'plot'
# mode = "filter"

# Assigning stocks
stocktags = Getdata.load_stock_list(tag)

# Assigning data
datamat = Loaddata.load(stocktags, tag)

if mode == 'plot' or mode == "filter":
    for stockname in stocktags.keys():

        print(stockname)

        # Initialize mode filter
        modefilter = []

        # Defining dataframe stock
        stock = datamat[stockname]

        # reverse pandas dataframe
        stock = stock.iloc[::-1]

        # Set datatypes to float64
        for column in ["Close", "Open", "Low", "High"]:
            stock[column] = stock[column].astype('float64')

        # Calculate Technical Indicators
        stock["RSI"] = ta.RSI(stock.Close.values, 14)
        stock["MA200"] = ta.SMA(stock.Close.values, 200)
        stock["MA200grad"] = np.gradient(stock["MA200"])
        stock["MA50"] = ta.SMA(stock.Close.values, 50)


        if mode == "filter":
            if stock["RSI"].iloc[-1] < 40 and stock["MA200grad"].iloc[-1] > 0:
                # Change mode to "plot"
                modefilter = "nofilter"


        # Formatting dates to ordinal
        stock["Dates2"] = stock["Dates"].apply(lambda x: x.toordinal())

        # Vectorizing properties
        x = 0
        y = len(stock["Dates2"])
        ohlc = []

        while x < y:
            append_me = stock["Dates2"][x], stock["Open"][x], stock["High"][x], stock["Low"][x], stock["Close"][x], \
                        stock["Volume"][x]
            ohlc.append(append_me)
            x += 1

        if mode == "plot" or modefilter == "nofilter":

            # --- Perform plotting ---

            # Subplots sharing both x-axes
            fig = plt.figure()
            ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
            ax1v = ax1.twinx()

            ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

            # Setting properties for first subplot
            candlestick_ohlc(ax1, ohlc, width=0.4, colorup='g', colordown='r')
            ax1.plot(stock["Dates"], stock["MA200"])
            ax1.plot(stock["Dates"], stock["MA50"])

            # Adding volume
            ax1v.fill_between(stock["Dates2"], 0, stock["Volume"], facecolor="c", alpha=0.4)
            ax1v.axes.yaxis.set_ticklabels([])
            ax1v.set_ylim(0, 2*stock["Volume"].max())

            # Adjusting axes properties
            ax1.set_title(stockname)
            ax1.set_ylabel("Close Price")
            ax1.grid()
            plt.setp(ax1.get_xticklabels(), visible=False)


            # Setting properties for second subplot
            ax2.plot(stock["Dates"], stock["RSI"])
            ax2.set_ylabel("RSI")
            ax2.grid()

            for label in ax2.xaxis.get_ticklabels():
                label.set_rotation(45)

            # Showing plot
            plt.show()
