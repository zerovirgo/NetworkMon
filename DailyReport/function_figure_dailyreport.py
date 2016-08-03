import os
import matplotlib
matplotlib.use('Agg')
import sys
sys.path.append('../NetworkDev')
import function_df
import pandas as pd
import pylab as plt
import numpy as np
import time
import timeModule


def exe(df,bigdf,refTime,filestring,start_sec= 0,end_sec= 0):
    print bigdf.columns
    querystr = 'index > 0'
    additionstr = ''
    if start_sec > 0.1:
        additionstr = '_%.0f_%.0f'%(start_sec-10,end_sec+10)

    msg = 'From {0} to {1}\n'.format(time.ctime(start_sec) , time.ctime(end_sec) )
    start_sec -= refTime
    end_sec -= refTime
    dicRoute = {
            'NorthRoute_AMS_CHI_AmsMLXe4' : 'North_AMS2CHI' ,
            'NorthRoute_CHI_AMS_ChiMLXe4' : 'North_CHI2AMS' ,
            'NorthRoute_CHI_TPE_ChiMLXe4' : 'North_CHI2TPE' ,
            'NorthRoute_TPE_CHI_TpeMLXe8' : 'North_TPE2CHI' ,
            'SouthRoute_AMS_CHI_AmsMLXe4' : 'South_AMS2CHI' ,
            'SouthRoute_CHI_AMS_ChiMLXe4' : 'South_CHI2AMS' ,
            'SouthRoute_CHI_TPE_ChiMLXe4' : 'South_CHI2TPE' ,
            'SouthRoute_TPE_CHI_TpeMLXe8' : 'South_TPE2CHI' }
    dicNumb = {
            'NorthRoute_AMS_CHI_AmsMLXe4' : 1 ,
            'NorthRoute_CHI_AMS_ChiMLXe4' : 2 ,
            'NorthRoute_CHI_TPE_ChiMLXe4' : 3 ,
            'NorthRoute_TPE_CHI_TpeMLXe8' : 4 ,
            'SouthRoute_AMS_CHI_AmsMLXe4' : 5 ,
            'SouthRoute_CHI_AMS_ChiMLXe4' : 6 ,
            'SouthRoute_CHI_TPE_ChiMLXe4' : 7 ,
            'SouthRoute_TPE_CHI_TpeMLXe8' : 8 }
    subQ = 'startT_sec >= {0} and startT_sec < ({0} + 86400)'.format(refTime)
    #print 'subQ=',subQ
    #subdf = bigdf.query('startT_sec >= {0} and startT_sec < ({1} )'.format(start_sec+refTime,end_sec+refTime))
    subdf = bigdf.query('endT_sec >= {0} and startT_sec < ({1} )'.format(start_sec+refTime,end_sec+refTime))
    subdf['refTimeStart'] = subdf['startT_sec'] - refTime
    subdf['refTimeEnd']   = subdf['endT_sec'] - refTime

    subdf['refTimeStart'].astype(np.int64)
    subdf['refTimeEnd'].astype(np.int64)
    group = pd.groupby(subdf, [subdf.route])
    for index,item in group.count()['endT'].iteritems():
        msg += '{0}: {1} flappings\n'.format(dicRoute[index],item)
    if start_sec > 0.1:
        querystr = 'index > {0} and index < {1}'.format(start_sec-10,end_sec+10)
    #print msg
    #print 'query and other str = ' , querystr 
    #print 'addition', additionstr
    #print 'start_sec = ' , start_sec
    #print 'total' , len(subdf) , 'togo'
    for index ,row in subdf.iterrows():
        #print 'start',int(row['refTimeStart']),'total ',int(row['refTimeStart'])-int(row['refTimeEnd']) , 'entries'
        #print 'time from ', time.ctime(row['startT_sec']), 'to', time.ctime(row['endT_sec'])
        #print 'route=' , row['route'], 'number = ',  dicNumb[row['route']]
        # in case start point goes below zero
        iStart = int(row['refTimeStart'])
        if row['refTimeStart'] < 0:
            iStart = 0
        df[row['route']].iloc[iStart:int(row['refTimeEnd'])+1] =  dicNumb[row['route']]
        #for i in range(int(row['refTimeStart']),int(row['refTimeEnd'])):
        #    df[row['route']][int(i)] = dicNumb[row['route']]
        #    #df.loc(row['route'],int(i)) = dicNumb[row['route']]
        #    if i%100 == 0:
        #        print i,'steps passed'

    #df[['NorthRoute_AMS_CHI_AmsMLXe4','NorthRoute_CHI_AMS_ChiMLXe4','NorthRoute_CHI_TPE_ChiMLXe4','NorthRoute_TPE_CHI_TpeMLXe8']].plot(kind='line',figsize=(12,9))
    #df.index = pd.date_range(filestring,periods = 86400, freq='s')
    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.20,0.05,0.78,0.75])
    print 'ctime = {0}'.format(time.ctime(refTime))
    df['timeIndex'] = pd.date_range(time.ctime(refTime),periods = 86400, freq='s')
    print 'lendf for draw =' , len(df[['timeIndex','SouthRoute_AMS_CHI_AmsMLXe4','SouthRoute_CHI_AMS_ChiMLXe4','SouthRoute_CHI_TPE_ChiMLXe4','SouthRoute_TPE_CHI_TpeMLXe8']].query(querystr))
    listDFindex = ['timeIndex','SouthRoute_AMS_CHI_AmsMLXe4', 'SouthRoute_CHI_AMS_ChiMLXe4',
                               'SouthRoute_CHI_TPE_ChiMLXe4', 'SouthRoute_TPE_CHI_TpeMLXe8',
                               'NorthRoute_AMS_CHI_AmsMLXe4', 'NorthRoute_CHI_AMS_ChiMLXe4',
                               'NorthRoute_CHI_TPE_ChiMLXe4', 'NorthRoute_TPE_CHI_TpeMLXe8' ]
    df[listDFindex].query(querystr).plot(kind='line',x = 'timeIndex', ax = ax, marker='o',markersize=1,color='blue',
            figsize=(12,9),ylim=(0,8.2), alpha = 0.5, legend=False)
    plt.yticks( np.arange(9) , ('','North_CHI2AmsMLXe4','North_AMS2ChiMLXe4','North_TPE2ChiMLXe4','North_CHI2TpeMLXe8',
        'South_CHI2AmsMLXe4','South_AMS2ChiMLXe4','South_TPE2ChiMLXe4','South_CHI2TpeMLXe8'))
    plt.xlabel('Date:{0}'.format(filestring))
    plt.title(msg)

    fpath = os.path.join(os.getcwd(),'Flapping{0}.png'.format(filestring+additionstr))
    plt.savefig(fpath)
    plt.clf()

    print fpath
    return
    #print df.head(20)

def getDays(seconds):
    import datetime
    #MM = int(datestring[4:6])
    #DD = int(datestring[6:])
    #print MM,DD
    MM = time.gmtime(seconds)[1]
    DD = time.gmtime(seconds)[2]
    print (datetime.datetime(2016,MM,DD)-datetime.datetime(2016,1,1)).days
    return (datetime.datetime(2016,MM,DD)-datetime.datetime(2016,1,1)).days
    
    return 
def drawDowntimeEventsToday(bigdf):
    yesterday = time.mktime(time.strptime(timeModule.getYesterday(),'%Y%m%d'))
    yesterday_sec = yesterday +28800.
    drawDowntimeEvents(bigdf,yesterday_sec,yesterday_sec+86400)
    #drawDowntimeEvents(getYesterday())
def drawDowntimeEvents(bigdf,start_sec,end_sec):
    #number = 86400
    number = 86400
    rTest = getDays(start_sec)
    tIndex = np.array(range(0,number))
    NorthRoute_AMS_CHI_AmsMLXe4 = np.zeros(number)
    NorthRoute_CHI_AMS_ChiMLXe4 = np.zeros(number)
    NorthRoute_CHI_TPE_ChiMLXe4 = np.zeros(number)
    NorthRoute_TPE_CHI_TpeMLXe8 = np.zeros(number)
    SouthRoute_AMS_CHI_AmsMLXe4 = np.zeros(number)
    SouthRoute_CHI_AMS_ChiMLXe4 = np.zeros(number)
    SouthRoute_CHI_TPE_ChiMLXe4 = np.zeros(number)
    SouthRoute_TPE_CHI_TpeMLXe8 = np.zeros(number)
    ser = pd.date_range('1/1/2016' ,periods = 365, freq='D')
    serNum = ser.astype(np.int64) // 10**9
    print ser[rTest], type(ser[rTest]), serNum[rTest],'{0}{1:0>2d}{2:0>2d}'.format( ser[rTest].year , ser[rTest].month , ser[rTest].day)
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
    datestr = '{0}{1:0>2d}{2:0>2d}'.format( ser[rTest].year , ser[rTest].month , ser[rTest].day)
    print 'datestr = ' , datestr
    exe(df,bigdf,start_sec-50,datestr,start_sec,end_sec)

#csvlist = [
#'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
#'SouthRoute_TPE_CHI_TpeMLXe8.csv'
#]
csvlist = [
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe8.csv'
]

dflist = []
for i in csvlist:
    dflist.append( function_df.getDF_netlog(i) )

newdf = function_df.getDF_netlog_total( dflist ).sort()

drawDowntimeEventsToday(newdf)
drawDowntimeEvents(newdf, 1470149625.0,1470150005.0)

#timelist = ana_FlappingBlocks2.exefunc(newdf)
#for item in timelist:
#    drawDowntimeEvents(newdf, item[0], item[1])
