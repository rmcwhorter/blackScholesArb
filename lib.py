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

def returnPriceArray(data, index=1):
    op = data.as_matrix()
    out = []
    for a in op:
        out.append(a[index])
    return out

#returns the Standard Deviation of the inputted array. STDEV is a useful measure of volatility
def stddev(arr):
    return numpy.stdev(arr)

#returns R^2 for the inputted array. R^2 is a useful measure of volatility
def r2(arr,indexArr, degree=15):
    #return numpy.poly1d(numpy.polyfit(arr, indexArr, degree))
    #slope, intercept, r_value, p_value, std_err = numpy.stats.linregress(x,y)
    #return r_value**2
    return numpy.corrcoef(arr, indexArr)

def beta(stock, benchmark):