import sys
sys.path.append("../")
import pandas as pd
import numpy
import mibian as m
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
from datetime import time
import pandas_market_calendars as mcal

import lib as lib

tckr = "EV"

sd = "1/1/1990"
ed = "15/1/2019"

historicalData = lib.returnPriceArray(si.get_data(tckr,sd,ed))
nyseCal = mcal.get_calendar("NYSE").schedule(start_date=sd, end_date=ed)
timeRange = nyseCal.iloc[:,1:].values
formattedTimeRange = []

for a in timeRange:
    o = str(a)
    o = o[0:10]
    formattedTimeRange.append(o)

formattedTimeRange = formattedTimeRange[1:]

print(len(historicalData) - len(formattedTimeRange))
plt.plot(historicalData,formattedTimeRange)

print("EOF")