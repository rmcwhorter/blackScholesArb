# -*- coding: utf-8 -*-

import mibian as m
from yahoo_fin import stock_info as si
import numpy
import pandas as pd
import requests
import arrow
import datetime

np = numpy

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
    return numpy.std(percentages)*numpy.sqrt(254) #NOTE: 254, though it seems contrived, is actually the number of trading days in a year.

#ticker is not case sensative
#assume we want 30 day volatility.
#Assume since 5 trading days in week, we return a span of 5/7 * 30 days by default. Will need to round up to greatest int
def getVolatilityTickerTime(ticker, startDate, endDate, index=4):
    #first we need to get our raw data
    raw = si.get_data(ticker, start_date=startDate, end_date=endDate).sort_values("date")
    #second we need to get historical prices.
    prices = returnPriceArray(raw, index=index)
    
    return volatility(prices)

#this is a method that takes something like 5.25B and returns 5250000000
def textToDollars(string):
    if(string == ("NaN" or "nan" or "na")):
        return "NaN"
    else:
        letter = string[-1:]
        numbers = string[:-1]
        factor = 0
        if(letter == "K"):
            factor = 1000
        if(letter == "M"):
            factor = 1000000
        if(letter == "B"):
            factor = 1000000000
        if(letter == "T"):
            factor = 1000000000000
        return factor*float(numbers)

#this method returns a Pandas DataFrame with all relevant information on the tickers
def dataFrameForTickers(tickers, startDate, endDate):
    prices = []
    volatility = []
    mktCap = []
    avgVol = []
    beta = []
    eps = []
    ev = []
    ebitda = []
    
    for a in tickers:
        try:
            x = returnQuote(a)
            prices.append(x)
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was returnQuote(a)")
            print("x = ", x)
        try:
            x = getVolatilityTickerTime(a,startDate,endDate)
            volatility.append(x)
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was getVolatilityTickerTime(a,startDate,endDate)")
            print("x = ", x)
        try:
            x = si.get_quote_table(a)
            q = x
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was si.get_quote_table(a)")
            print("x = ", x)
        try:
            x = q["Market Cap"]
            mktCap.append(textToDollars(x))
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was q[\"Market Cap\"]")
            print("x = ", x)
        try:
            x = q["Avg. Volume"]
            avgVol.append(q["Avg. Volume"])
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was q[\"Avg. Volume\"]")
            print("x = ", x)
        try:
            x = q["Beta (3Y Monthly)"]
            beta.append(x)
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was q[\"Beta (3Y Monthly)\"]")
            print("x = ", x)
        try:
            x = q["EPS (TTM)"]
            eps.append(x)
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was q[\"EPS (TTM)\"]")
            print("x = ", x)
        try:
            x = si.get_stats(a)
            p = x
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was si.get_stats(a)")
            print("x = ", x)
        try:
            x = p.iloc[1]['Value']
            y = textToDollars(x)
            ev.append(y)
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was textToDollars(p.iloc[1]['Value'])")
            print("x = ", x)
            print("y = ", y)
        try:
            x = p.iloc[19]['Value']
            ebitda.append(x)
            print("Success")
        except:
            print("Failed on ", a)
            print("Step was p.iloc[19]['Value']")
            print("x = ", x)
    
    d = {'Ticker' : tickers,
         'Price' : prices,
         'Market Cap' : mktCap,
         'EPS' : eps,
         'Avg. Vol.' : avgVol,
         'ß' : beta,
         'Volatility' : volatility,
         'Enterprise Value' : ev,
         'EBITDA' : ebitda
         }
    
    frame = pd.DataFrame(d)
    return frame

def vol2(arr):
    o = 0
    for a in range(len(arr)):
        o += np.abs((arr[a+1]/arr[a])-1)
    return o/len(arr)

def get_quote_data(symbol='AAPL', data_range='1d', data_interval='1m'):
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
    data = res.json()
    body = data['chart']['result'][0]    
    dt = datetime.datetime
    dt = pd.Series(map(lambda x: arrow.get(x).to('US/Central').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
    dg = pd.DataFrame(body['timestamp'])    
    df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
    df.dropna(inplace=True)     #removing NaN rows
    df.columns = ['OPEN', 'HIGH','LOW','CLOSE','VOLUME']    #Renaming columns in pandas
    
    return df
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        