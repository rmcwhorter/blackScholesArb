# -*- coding: utf-8 -*-

import pandas as pd
import numpy
import mibian as m
from yahoo_fin import stock_info as si

import lib

#currentPrice = si.get_live_price("aapl")

tickers = ["aapl","nvda","amzn"]

sd = '11/3/2018'
ed = '12/3/2018'

tckr = "pypl"
currentPrice = 85.09 #si.get_live_price(tckr)

volatility = lib.getVolatilityTickerTime(tckr,sd,ed)

print(currentPrice)

option = m.BS([currentPrice,86,2.25,17], volatility=(volatility*100))

print()
print("Volatility ", volatility)
print()
print("Call Price ", option.callPrice)
print()
print("Delta ", option.callDelta)
print("Gamma ", option.gamma)
print("Theta ", option.callTheta)
print("Vega ", option.vega)
print("Rho ", option.callRho)
print()
print()
print()