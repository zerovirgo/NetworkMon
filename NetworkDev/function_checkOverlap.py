import pandas as pd
import os
import function_df



csvlist = [
'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe8.csv'
]


dflist = []
for i in csvlist:
    print i
    dflist.append(function_df.getDF_netlog(i))

myDF = function_df.getDF_netlog_total(dflist) 
