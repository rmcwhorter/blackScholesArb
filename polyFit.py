import mibian as m
from yahoo_fin import stock_info as si
import numpy as np
import pandas as pd
import lib as lib
import matplotlib.pyplot as plt

data = lib.get_quote_data('EV', '7d', '1m')
#print(data)

t = []
Open = data['OPEN'].values
High = data['HIGH'].values
Low = data['LOW'].values
Close = data['CLOSE'].values
Volume = data['VOLUME'].values

for a in range(len(Open)): t.append(a)

p = np.polyfit(Open,t,10)
print(p)

def f(t,p,x=0):
    o = 0
    for a in range(len(p)):
        o += (p[a]*(t**a))+x
    return o

out = []
for b in t:
    out.append(f(b,p,x=Open[0]))

plt.plot(t,Open)
#plt.plot(t,out)

print("EOF")