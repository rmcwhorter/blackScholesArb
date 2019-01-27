import lib
from yahoo_fin import stock_info as si
import numpy as np
import pandas as pd
import arrow
import datetime
import pickle

fRawData = "nasdaq/nasdaqRaw.pkl"
fFundamentalsByTicker = "nasdaq/tickerFundamentals.pkl"
fFundamentalsNasdaq = "nasdaq/nasdaqFundamentals.pkl"

with open(fRawData, 'rb') as handle:tickerRawData = pickle.load(handle)
with open(fFundamentalsByTicker, 'rb') as handle:tickerFundamentals = pickle.load(handle)
with open(fFundamentalsNasdaq, 'rb') as handle:nasdaqFundamentals = pickle.load(handle)

#Compute Beta relative to ^IXIC for each ticker.
mkt = tickerRawData["^IXIC"]["CLOSE"].values
for a in tickerFundamentals:
    try: beta = np.cov(tickerRawData[a]["CLOSE"].values,mkt) / np.var(mkt)
    except: beta = np.nan
    
    if(a != "^IXIC"): tickerFundamentals[a]["Beta"] = beta
    else: tickerFundamentals[a]["Beta"] = 1

print(pd.Series(tickerFundamentals["EDIT"]))
print()
print(pd.Series(tickerFundamentals["^IXIC"]))
print()
print(tickerFundamentals["^IXIC"]["Beta"])



#Write any new changes to the data
with open(fRawData, 'wb') as handle: pickle.dump(tickerRawData, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open("nasdaq/tickerFundamentals.pkl", 'wb') as handle: pickle.dump(tickerFundamentals, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open("nasdaq/nasdaqFundamentals.pkl", 'wb') as handle: pickle.dump(nasdaqFundamentals, handle, protocol=pickle.HIGHEST_PROTOCOL)

#End of File
print("EOF")