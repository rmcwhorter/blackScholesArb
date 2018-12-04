# -*- coding: utf-8 -*-

import pandas as pd
import numpy
import mibian as m
from yahoo_fin import stock_info as si

import lib

currentPrice = si.get_live_price("aapl")

tickers = ["aapl","nvda","amzn"]

sd = '11/26/2018'
ed = '11/30/2018'

data = si.get_data("aapl", start_date=sd, end_date=ed)

index = si.get_data("^gspc", start_date=sd, end_date=ed)

def returnPriceArray(data, index=1):
    op = data.as_matrix()
    out = []
    for a in op:
        out.append(a[index])
    return out

aaplOpen = returnPriceArray(data)
snpOpen = returnPriceArray(index)

r2 = lib.r2(aaplOpen, snpOpen)

print(r2)