import lib
from yahoo_fin import stock_info as si
import numpy
import pandas as pd
import arrow
import datetime
import pickle
import sys

np = numpy

file = "nasdaq/nasdaqRaw.pkl"
with open(file, 'rb') as handle:tickerRawData = pickle.load(handle)

#set up tickerFundamentals
tickerFundamentals = {}
for a in tickerRawData:
    tickerFundamentals[a] = {}

#Set up Nasdaq fundamentals
nasdaqFundamentals = {}

#get average volume for each ticker
for a in tickerFundamentals:
    try: avg = numpy.mean(tickerRawData[a]["VOLUME"].values)
    except: avg = np.nan
    tickerFundamentals[a]["avgVol"] = avg


#get average volume at t = 8:30:00 AM. Compute AVT0 / AvgVol
for a in tickerFundamentals:
    try: d = tickerRawData['AAPL']["VOLUME"].filter(like="8:30:00")
    except: print("Failure at 'd = tickerRawData['AAPL'][\"VOLUME\"].filter(like=\"8:30:00\")'.")
    
    try: e = numpy.mean(d.values)/tickerFundamentals[a]["avgVol"]
    except: e = np.nan
    
    tickerFundamentals[a]["VolT0 / avgVol"] = e

#Compute Average AVT0 / AvgVol
o = []
for a in tickerFundamentals:
    d = tickerFundamentals[a]["VolT0 / avgVol"]
    if(isinstance(d, float) and d != np.Inf and d != np.nan): o.append(d)

#Compute shares outstanding for each stock.
for a in tickerFundamentals:
    try: mktCap = lib.textToDollars(si.get_quote_table(a)["Market Cap"])
    except: mktCap = np.nan
    
    try: p = si.get_live_price(a)
    except: p = np.nan
    
    try: sharesOutstanding = mktCap/p
    except: sharesOutstanding = np.nan
    
    tickerFundamentals[a]["Shares Outstanding"] = sharesOutstanding
    print(a)
    

#compute standard deviation for High, Low, Open, Close, Volume
for a in tickerFundamentals:
    try: hStdDev = np.std(tickerRawData[a]["HIGH"].values)
    except: hStdDev = np.nan
    
    try: lStdDev = np.std(tickerRawData[a]["LOW"].values)
    except: lStdDev = np.nan
    
    try: oStdDev = np.std(tickerRawData[a]["OPEN"].values)
    except: oStdDev = np.nan
    
    try: cStdDev = np.std(tickerRawData[a]["CLOSE"].values)
    except: cStdDev = np.nan
    
    try: vStdDev = np.std(tickerRawData[a]["VOLUME"].values)
    except: vStdDev = np.nan
    
    tickerFundamentals[a]["High 1m STDEV"] = hStdDev
    tickerFundamentals[a]["Low 1m STDEV"] = lStdDev
    tickerFundamentals[a]["Open 1m STDEV"] = oStdDev
    tickerFundamentals[a]["Close 1m STDEV"] = cStdDev
    tickerFundamentals[a]["Volume 1m STDEV"] = vStdDev

#compute average 1m StdDev for High, Low, Open, Close, Volume for every ticker
h = []
l = []
o = []
c = []
v = []
for a in tickerFundamentals:
    try: hTmp = tickerFundamentals[a]["High 1m STDEV"]
    except: hTmp = np.nan
    if(hTmp != np.nan): h.append(hTmp)
    
    try: lTmp = tickerFundamentals[a]["Low 1m STDEV"]
    except: lTmp = np.nan
    if(lTmp != np.nan): l.append(lTmp)
    
    try: oTmp = tickerFundamentals[a]["Open 1m STDEV"]
    except: oTmp = np.nan
    if(oTmp != np.nan): o.append(oTmp)
    
    try: cTmp = tickerFundamentals[a]["Close 1m STDEV"]
    except: cTmp = np.nan
    if(cTmp != np.nan): c.append(cTmp)
    
    try: vTmp = tickerFundamentals[a]["Volume 1m STDEV"]
    except: vTmp = np.nan
    if(vTmp != np.nan): v.append(vTmp)

nasdaqFundamentals["AVG High 1m STDEV"] = np.mean(h)
nasdaqFundamentals["AVG Low 1m STDEV"] = np.mean(l)
nasdaqFundamentals["AVG Open 1m STDEV"] = np.mean(o)
nasdaqFundamentals["AVG Close 1m STDEV"] = np.mean(c)
nasdaqFundamentals["AVG Volume 1m STDEV"] = np.mean(v)
    
    

nasdaqFundamentals["Average (VolT0 / avgVol)"] = numpy.mean(o)
    

print("tickerFundamentals['AAPL']: ",tickerFundamentals['AAPL'])
print()
print("nasdaqFundamentals: ",nasdaqFundamentals)

with open("nasdaq/tickerFundamentals.pkl", 'wb') as handle: pickle.dump(tickerFundamentals, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open("nasdaq/nasdaqFundamentals.pkl", 'wb') as handle: pickle.dump(nasdaqFundamentals, handle, protocol=pickle.HIGHEST_PROTOCOL)



print("EOF")