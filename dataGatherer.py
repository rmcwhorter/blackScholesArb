import lib
from yahoo_fin import stock_info as si
import numpy
import pandas as pd
import arrow
import datetime
import pickle

nasdaq = si.tickers_nasdaq()
#print(nasdaq)

rawData = {}

for a in nasdaq:    
        try:
            d = lib.get_quote_data(a, '5d', '1m')
            rawData[a] = d
            print("Success on ", a)
        except:
            print("Failed on ",a)

print(d)

file = "nasdaq/nasdaqRaw.pkl"

with open(file, 'wb') as handle: pickle.dump(rawData, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("EOF")