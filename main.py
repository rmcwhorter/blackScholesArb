# -*- coding: utf-8 -*-

import pandas as pd
import numpy
import mibian as m
from yahoo_fin import stock_info as si

import lib as lib

pd.set_option('display.max_columns', 30)

#["TRP","EC","MPLX","FLT","IBKR","WEC","IMO","CQP","VRSK","CHKP","PBA","RMD"]
screener = []

traweek = ["TPL","MO","EV","LSTR","PAYX","MMM","HSY","ROL","FDS","SHW","PEP","TJX","ACN"]

pharma = ["SPHS","CRSP","SGMO","NTLA","ACRX","ARNA","FLDM","ILMN","PACB","QGEN","ATHN","INVE","AMRN","EDIT","CELG","BIIB","REGN"]

tickers = screener + traweek + pharma

sd = '11/3/2018'
ed = '15/1/2019'

print("running")

screenerFrame = lib.dataFrameForTickers(screener, sd, ed)
pharmaFrame = lib.dataFrameForTickers(pharma, sd, ed)
traweekFrame = lib.dataFrameForTickers(traweek, sd, ed)

frames = [screenerFrame, pharmaFrame, traweekFrame]

writer = pd.ExcelWriter("output.xlsx")
screenerFrame.to_excel(writer,"Screener")
#pharmaFrame.to_excel(writer,"Pharma")
#traweekFrame.to_excel(writer,"Traweek")
writer.save()

print()
print("End File")
