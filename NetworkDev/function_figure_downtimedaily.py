import os
import matplotlib
matplotlib.use('Agg')
import function_df
import pandas as pd
import pylab as plt
import numpy as np
import time

def exe(df,bigdf,refTime,filestring):
    print bigdf.columns
    dicNumb = {
            'NorthRoute_AMS_CHI_AmsMLXe4' : 1 ,
            'NorthRoute_CHI_AMS_ChiMLXe4' : 2 ,
            'NorthRoute_CHI_TPE_ChiMLXe4' : 3 ,
            'NorthRoute_TPE_CHI_TpeMLXe8' : 4 ,
            'SouthRoute_AMS_CHI_AmsMLXe4' : 5 ,
            'SouthRoute_CHI_AMS_ChiMLXe4' : 6 ,
            'SouthRoute_CHI_TPE_ChiMLXe4' : 7 ,
            'SouthRoute_TPE_CHI_TpeMLXe8' : 8 }
    subdf = bigdf.query('startT_sec >= {0} and startT_sec < ({0} + 86400)'.format(refTime))
    subdf['refTimeStart'] = subdf['startT_sec'] - refTime
    subdf['refTimeEnd']   = subdf['endT_sec'] - refTime

    subdf['refTimeStart'].astype(np.int64)
    subdf['refTimeEnd'].astype(np.int64)
    print 'total' , len(subdf) , 'togo'
    for index ,row in subdf.iterrows():
        print 'start',int(row['refTimeStart']),'total ',int(row['refTimeStart'])-int(row['refTimeEnd']) , 'entries'
        for i in range(int(row['refTimeStart']),int(row['refTimeEnd'])):
            df[row['route']][int(i)] = dicNumb[row['route']]
    print 'chedk1'

    #df[['NorthRoute_AMS_CHI_AmsMLXe4','NorthRoute_CHI_AMS_ChiMLXe4','NorthRoute_CHI_TPE_ChiMLXe4','NorthRoute_TPE_CHI_TpeMLXe8']].plot(kind='line',figsize=(12,9))
    #df.index = pd.date_range(filestring,periods = 86400, freq='s')
    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.20,0.05,0.78,0.75])
    df['timeIndex'] = pd.date_range(filestring,periods = 86400, freq='s')
    df[['timeIndex','SouthRoute_AMS_CHI_AmsMLXe4','SouthRoute_CHI_AMS_ChiMLXe4','SouthRoute_CHI_TPE_ChiMLXe4','SouthRoute_TPE_CHI_TpeMLXe8']].query('index > 26500 and index < 27000').plot(kind='line',x = 'timeIndex', ax = ax,
            figsize=(12,9),ylim=(0,8.2), alpha = 0.5, legend=False)
    plt.yticks( np.arange(9) , ('','North_CHI_AmsMLXe4','North_AMS_ChiMLXe4','North_TPE_ChiMLXe4','North_CHI_TpeMLXe8',
        'South_CHI_AmsMLXe4','South_AMS_ChiMLXe4','South_TPE_ChiMLXe4','South_CHI_TpeMLXe8'))
    plt.xlabel('Date:{0}'.format(filestring))

    print 'chedk2'
    plt.savefig('/nfs/home/zero/Projects/NetworkMon/NetworkDev/Flapping{0}.png'.format(filestring))
    print 'chedk3'
    #print df.head(20)

def drawDowntimeDayly(bigdf):
    #number = 86400
    number = 86400
    rTest = 178
    tIndex = np.array(range(0,number))
    NorthRoute_AMS_CHI_AmsMLXe4 = np.zeros(number)
    NorthRoute_CHI_AMS_ChiMLXe4 = np.zeros(number)
    NorthRoute_CHI_TPE_ChiMLXe4 = np.zeros(number)
    NorthRoute_TPE_CHI_TpeMLXe8 = np.zeros(number)
    SouthRoute_AMS_CHI_AmsMLXe4 = np.zeros(number)
    SouthRoute_CHI_AMS_ChiMLXe4 = np.zeros(number)
    SouthRoute_CHI_TPE_ChiMLXe4 = np.zeros(number)
    SouthRoute_TPE_CHI_TpeMLXe8 = np.zeros(number)
    ser = pd.date_range('1/1/2016' ,periods = 193, freq='D')
    serNum = ser.astype(np.int64) // 10**9
    print ser[rTest], type(ser[rTest]), serNum[rTest],'{0}{1:0>2d}{2}'.format( ser[rTest].year , ser[rTest].month , ser[rTest].day)
    df = pd.DataFrame({'timeser':tIndex,
            'NorthRoute_AMS_CHI_AmsMLXe4' : NorthRoute_AMS_CHI_AmsMLXe4 ,
            'NorthRoute_CHI_AMS_ChiMLXe4' : NorthRoute_CHI_AMS_ChiMLXe4 ,
            'NorthRoute_CHI_TPE_ChiMLXe4' : NorthRoute_CHI_TPE_ChiMLXe4 ,
            'NorthRoute_TPE_CHI_TpeMLXe8' : NorthRoute_TPE_CHI_TpeMLXe8 ,
            'SouthRoute_AMS_CHI_AmsMLXe4' : SouthRoute_AMS_CHI_AmsMLXe4 ,
            'SouthRoute_CHI_AMS_ChiMLXe4' : SouthRoute_CHI_AMS_ChiMLXe4 ,
            'SouthRoute_CHI_TPE_ChiMLXe4' : SouthRoute_CHI_TPE_ChiMLXe4 ,
            'SouthRoute_TPE_CHI_TpeMLXe8' : SouthRoute_TPE_CHI_TpeMLXe8 })
    #print df.head()
    datestr = '{0}{1:0>2d}{2}'.format( ser[rTest].year , ser[rTest].month , ser[rTest].day)
    exe(df,bigdf,serNum[rTest],datestr)

csvlist = [
'NorthRoute_AMS_CHI_AmsMLXe4.csv' ,
'NorthRoute_CHI_AMS_ChiMLXe4.csv' ,
'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
'SouthRoute_AMS_CHI_AmsMLXe4.csv' ,
'SouthRoute_CHI_AMS_ChiMLXe4.csv' ,
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe8.csv'
]

dflist = []
for i in csvlist:
    dflist.append( function_df.getDF_netlog(i) )

newdf = function_df.getDF_netlog_total( dflist ).sort()

drawDowntimeDayly(newdf)
