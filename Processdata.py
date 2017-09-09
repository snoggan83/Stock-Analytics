import Getdata
import Loaddata
from matplotlib import pyplot as plt

# Initializing Properties

# Stock tag
tag = 'LargeCap'
# tag = 'MidCap'
# tag = 'SmallCap'
# tag = 'Commodities'
# tag = 'Index'

#  Running mode
mode = 'plot'

# Assigning stocks
stocktags = Getdata.load_stock_list(tag)

# Assigning data
datamat = Loaddata.load(stocktags, tag)

if mode == 'plot':
    for stockname in stocktags.keys():

        # Defining dataframe stock
        stock = datamat[stockname]

        for column in ["Close", "Open", "Low", "High"]:
            stock[column] = stock[column].astype('float64')

        plt.plot(stock['Dates'], stock["Close"])
        plt.show()

