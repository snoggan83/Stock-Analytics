import json
from Getdata import *

"""Getdata.py: Imports LargeCap, MidCap, SmallCap, Index and Commodities tags for the Swedish Stock market. Converts the dictionaries to JSON format"""

__author__      = "John Nilsson"
__copyright__   = "Copyright 2017, Project Stock Trade"


#  Call Different Stocklists
stocklists = ["LargeCap", "MidCap", "SmallCap"]
count = 1
count_list = 1
for stocklist in stocklists:

    data = []
    stocklistdict = load_stock_list(stocklist)

    for key in stocklistdict.keys():
        dict_temp = {"model": "stocklist.stock", "pk": count, "fields": {"stocklist": count_list, "stock_title": key,
                                                                         "stocktag_str": stocklistdict[key][1],
                                                                         "stocktag_num": int(stocklistdict[key][0]),
                                                                         "in_portfolio": False}}
        count += 1
        data.append(dict_temp)

    # Print to file
    with open(stocklist + "Data.json", "w") as outfile:
        json.dump(data, outfile)

    # Increase count
    count_list += 1
