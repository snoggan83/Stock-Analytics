import urllib
import os.path
from datetime import datetime, date
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

url1 = "http://www.euroinvestor.se/stock/historicalquotes.aspx?instrumentId="
url2 = "&format=CSV"
savepath = 'C:\Users\John\PycharmProjects\untitled2'
savepathtest = 'C:\\Users\John\\PycharmProjects\\untitled2\\test'



def load(stocktags, tag):
    # Stock Book
    stockbook = {}

    # Initializing dateparser
    dateparse_now = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

    for stockname in stocktags.keys():

        # Assign Filename
        file_name = stockname
        file_path = os.path.join(savepath, tag, file_name + ".txt")

        # Load files from repository

        if os.path.exists(file_path):
            file_mod_timestamp = datetime.strftime(datetime.fromtimestamp(os.path.getmtime(file_path)), '%Y-%m-%d')
            today = str(date.today())

            if today == file_mod_timestamp:

                # Read file
                data = pd.read_csv(file_path,  delimiter=';', decimal=",", skiprows=1, names=["Dates", "Open", "High", "Low", "Close", "Volume"],
                                   parse_dates=['Dates'], date_parser=dateparse, na_filter=True, skip_blank_lines=True, dtype={"Volume": np.float64})

                # Write data to Dictionary
                stockbook[stockname] = data
                continue

        # Concatenating URL
        urlfull = url1 + stocktags[stockname][0] + url2
        count = 0
        err_count = 0

        # Load data from file
        while count == err_count:
            try:
                f = urllib.urlopen(urlfull)

                data_now = pd.read_csv(f,  delimiter=';', names=["Dates", "Open", "High", "Low", "Close", "Volume"]
                                 ,usecols=range(0, 6), decimal=",", skiprows=1, dtype={'Open': np.float64,
                                                                                        'High': np.float64,
                                                                                        'Low': np.float64,
                                                                                        'Close': np.float64,
                                                                                        'Volume': np.int64},
                                       parse_dates=['Dates'], date_parser=dateparse_now)

                f.close()
            except IOError:
                print 'cannot open', urlfull
                err_count += 1
            count += 1

            if os.path.exists(file_path):

                # Print stock name
                print(stockname)

                # data_hist = pd.read_csv(f,  delimiter=';', names=["Dates", "Open", "High", "Low", "Close", "Volume"]
                #                  , usecols=range(0, 6), decimal=",", skiprows=1, dtype={'Open': np.float64,
                #                                                                         'High': np.float64,
                #                                                                         'Low': np.float64,
                #                                                                         'Close': np.float64,
                #                                                                         'Volume': np.int64},
                #                        parse_dates=['Dates'], date_parser=dateparse)
                #
                #
                # # format time data
                # hist_dates = [datetime.strptime(r1, '%Y-%m-%d %H:%M:%S') for r1 in data_hist["Dates"]]
                # hist_dates_format = [datetime.strftime(r2, '%Y-%m-%d') for r2 in hist_dates]
                #
                # hist_date_last = datetime.strptime(data_now["Dates"].iloc[-1], '%Y-%m-%d %H:%M:%S')
                # hist_date_last_format = datetime.strftime(hist_date_last, '%Y-%m-%d')
                #
                # # Locate last data on current date in historical date
                # nr_rows = hist_dates_format.index(hist_date_last_format)
                #
                # # Format hist data data frame
                # data_hist_format = data_hist.iloc[nr_rows+1:-1]
                #
                # # Concatenate data frames
                # data = pd.concat([data_now, data_hist_format])
                #
                # # Write data to Dict
                # stockbook[stockname] = data

                # Write data to file
                data_now.to_csv(file_path, index=False, sep=";")

            else:

                # Print stock name
                print(stockname + " Added to dir")

                # Write data to file
                data_now.to_csv(file_path, index=False)

                # Write data to Dict
                stockbook[stockname] = data_now

    # Return Stockbook
    return stockbook
