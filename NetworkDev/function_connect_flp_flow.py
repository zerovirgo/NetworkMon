# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 07:29:11 2016

@author: kschen
"""

import pandas as pd
import numpy as np
import function_df

def createCSVmod1(dfFlp,dfFlow,outname = 'shggg'):
    iF = 0 
    iMax = len(dfFlow.index)-1
    iFlow = dfFlow.index
    fout = open(outname+'.csv','w')
    fout.writelines('startT,endT,startT_sec,endT_sec,duration,interval,interface,\
    reason,route,netlogtime,nettimediff,netinput,netoutput\n')
    for index, row in dfFlp.iterrows():
        if iF >= iMax:break
        #Find the first time later then the down time
        while row['startT_sec'] > dfFlow['abstime'][iFlow[iF]]:
            iF += 1
            if iF >= iMax:break
        #once found, back to previous one,i.e most close to the down time
        else:
            iF -= 1
            writeline = \
            '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}\n'.format(str(index),
            row['endT'],row['startT_sec'],row['endT_sec'],row['duration'],
            row['interval'],row['interface'],row['reason'],row['route'],
            dfFlow['date'][iFlow[iF]],(row['startT_sec']-dfFlow['abstime'][iFlow[iF]]),
            dfFlow['input'][iFlow[iF]], dfFlow['output'][iFlow[iF]])
            fout.writelines(writeline)
    fout.close()



# 'NorthRoute_AMS_CHI_AmsMLXe4.csv' ,
# 'NorthRoute_CHI_AMS_ChiMLXe4.csv' ,
# 'SouthRoute_CHI_AMS_ChiMLXe4.csv' ,
# 'SouthRoute_AMS_CHI_AmsMLXe4.csv' ,
fnlist = [
'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe4.csv'
]
lnlist = [
    'chi2tpe_link12016.csv' , 
    'tpe2chi_link12016.csv' , 
    'chi2tpe_link22016.csv' , 
    'tpe2chi_link22016.csv'
]

for item in zip(fnlist,lnlist):
    df1 = function_df.getDF_netlog(item[0])
    df2 = function_df.getDF_netflow(item[1])
    print item[1]
    iX = df1.index
    queryString = 'abstime > {0} & abstime <={1}'.format(df1.startT_sec[iX[0]],df1.startT_sec[iX[-1]])
    print 'avg input = ' , df2.query(queryString).input.mean()
    print 'avg output = ' , df2.query(queryString).output.mean()
    print 
    #createCSVmod1(df1,df2,'mod1_'+item[0].split('.csv')[0])

#df1 = function_df.getDF_netlog(fnlist[-1])
#df2 = function_df.getDF_netflow('tpe2chi_link22016.csv')
#createCSVmod1(df1,df2)



#for item in zip(fnlist,lnlist):
#    df1 = function_df.getDF_netlog(item[0])
#    df2 = function_df.getDF_netflow(item[1])
#    createCSVmod1(df1,df2,'mod1_'+item[0].split('.csv')[0])
