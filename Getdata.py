import requests
from bs4 import BeautifulSoup

# Author: John Nilsson
# Date: 2017-11-06

# """Getdata.py: Scrapes data from EuroInvestor"""
#
# __author__      = "John Nilsson"
# __copyright__   = "Copyright 2016, Project Stock Trade"


def scrape_list(list_obj):

    # EuroInvestor
    base_url = "http://www.euroinvestor.com/markets/stocks/europe/sweden/"

    # Assign main URL
    main_url = requests.get(base_url + list_obj)

    # Create Soup object
    soup = BeautifulSoup(main_url.content, "lxml")

    # Define variables
    stock_title = []
    stock_id = []

    for link in soup.find_all("a"):
        # Scrape links from "EuroInvestor" Website
        if "/exchanges" in link.get("href") and link.get('title'):

            stock_title_temp = link.get('title')
            stock_id_temp = link.get("href").rsplit('/', 1)[-1]

            non_conv_char = "/\?%"
            for char in non_conv_char:
                if char in stock_title_temp:
                    stock_title_temp = stock_title_temp.replace(char, "")

            non_conv_char2 = "åÅäÄöÖ"
            for char in non_conv_char2:
                if char in stock_title_temp:
                    if char == "Å" or char == "Ä":
                        stock_title_temp = stock_title_temp.replace(char, "A")
                    if char == "å" or char == "ä":
                        stock_title_temp = stock_title_temp.replace(char, "a")
                    if char == "Ö":
                        stock_title_temp = stock_title_temp.replace(char, "O")
                    if char == "ö":
                        stock_title_temp = stock_title_temp.replace(char, "o")

            stock_title.append(stock_title_temp)
            stock_id.append(stock_id_temp)

    # Create dictionary
    stdict = dict(zip(stock_title, stock_id))

    # Return dictionary
    return stdict