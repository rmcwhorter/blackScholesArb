# -*- coding: utf-8 -*-

import mibian as m
from yahoo_fin import stock_info as si
import numpy

def returnQuotes(tickers):
    out = []
    for a in tickers:
        out.append(returnQuote(a))
    return out
    
def returnQuote(ticker):
    return si.get_live_price(ticker)

def returnPriceArray(data, index=4):
    #[open,high,low,close,adjclose,volume,ticker]
    op = data.values
    out = []
    for a in op:
        out.append(a[index])
    return out

#returns R^2 for the inputted array. R^2 is a useful measure of volatility
def r2(arr,indexArr, degree=15):
    #return numpy.poly1d(numpy.polyfit(arr, indexArr, degree))
    #slope, intercept, r_value, p_value, std_err = numpy.stats.linregress(x,y)
    #return r_value**2
    return numpy.corrcoef(arr, indexArr)

def volatility(arr):
    percentages = []
    for a in range(len(arr)):
        percentages.append((arr[a]/arr[a-1])-1)
    return numpy.std(percentages)*numpy.sqrt(254)

#ticker is not case sensative
#assume we want 30 day volatility.
#Assume since 5 trading days in week, we return a span of 5/7 * 30 days by default. Will need to round up to greatest int
def getVolatilityTickerTime(ticker, startDate, endDate, index=4):
    #first we need to get our raw data
    raw = si.get_data(ticker, start_date=startDate, end_date=endDate).sort_values("date")
    #second we need to get historical prices.
    prices = returnPriceArray(raw, index=index)
    
    return volatility(prices)

