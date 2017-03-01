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
from matplotlib.ticker import NullFormatter
import ana_FlappingBlocks


def markduration(infos):
    print 'marking',infos
    plt.text(infos[1],infos[2],'{0}'.format(infos[0]),ha='left',va='bottom',rotation=90,fontsize=10)

def dateparse (time_in_secs):
    import datetime
    return datetime.datetime.fromtimestamp(float(time_in_secs))

def exe2(bigdf,datestr):
    from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
    from matplotlib.dates import datestr2num 
    dicRoute = {
            'NorthRoute_AMS_CHI_AmsMLXe4' : 'North_AmsMLXe4_CHI' ,
            'NorthRoute_CHI_AMS_ChiMLXe4' : 'North_ChiMLXe4_AMS' ,
            'NorthRoute_CHI_TPE_ChiMLXe4' : 'North_ChiMLXe4_TPE' ,
            'NorthRoute_TPE_CHI_TpeMLXe8' : 'North_TpeMLXe8_CHI' ,
            'SouthRoute_AMS_CHI_AmsMLXe4' : 'South_AmsMLXe4_CHI' ,
            'SouthRoute_CHI_AMS_ChiMLXe4' : 'South_ChiMLXe4_AMS' ,
            'SouthRoute_CHI_TPE_ChiMLXe4' : 'South_ChiMLXe4_TPE' ,
            'SouthRoute_TPE_CHI_TpeMLXe8' : 'South_TpeMLXe8_CHI' }
    dicNumb = {
            'NorthRoute_AMS_CHI_AmsMLXe4' : 1 ,
            'NorthRoute_CHI_AMS_ChiMLXe4' : 2 ,
            'NorthRoute_CHI_TPE_ChiMLXe4' : 3 ,
            'NorthRoute_TPE_CHI_TpeMLXe8' : 4 ,
            'SouthRoute_AMS_CHI_AmsMLXe4' : 5 ,
            'SouthRoute_CHI_AMS_ChiMLXe4' : 6 ,
            'SouthRoute_CHI_TPE_ChiMLXe4' : 7 ,
            'SouthRoute_TPE_CHI_TpeMLXe8' : 8 }
    print bigdf.columns
    # draw an empty plot if no flapping
    if len(bigdf) == 0:
            print 'nothing to plot'
            plt.figure(1, figsize=(12,9))
            ax = plt.axes([0.20,0.05,0.78,0.75])
            plt.title('No flapping events today')
            fpath = os.path.join(os.getcwd(),'Flapping{0}.png'.format(filestring+additionstr))
            plt.savefig(fpath)
            plt.clf()
            return

    bigdf['startdate'] = bigdf['startT_sec'].apply(lambda x:dateparse(x))
    bigdf['enddate'] = bigdf['endT_sec'].apply(lambda x:dateparse(x))
    bigdf['durationindex'] = bigdf['duration'].apply(lambda x: str(int(x)))
    #print bigdf['durationindex'].value_counts().sort_values(ascending=False)
    group = pd.groupby(bigdf, [bigdf.route])
    msg = 'Date: {0}\n'.format( datestr )
    for index,item in group.count()['endT'].iteritems():
        msg += '{0}: {1} flappings\n'.format(dicRoute[index],item)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for index,row in bigdf.query('duration==0').iterrows():
        #print row['startdate'] , type(row['startdate']) , str(row['startdate'])
        x1.append(datestr2num(str(row['startdate'])))
        y1.append(dicNumb[row['route']])
    for index,row in bigdf.query('duration>0').iterrows():
        x2.append(datestr2num(str(row['startdate'])))
        y2.append(dicNumb[row['route']])

    #bigdf.query('duration==0')['']
    #bigdf.query('duration>0')
    fig, ax = plt.subplots(figsize=(12,9))
    # clean empty plot
    plt.clf()
    ax = plt.axes([0.20,0.12,0.75,0.70])
    ax.plot_date(x1, y1, color='blue',markersize=1)
    ax.plot_date(x2, y2, color='red',markersize=1)
    ax.set_xlim(datestr2num(datestr),datestr2num(datestr)+1)
    ax.set_ylim([0,8.5])
    #print ax.get_xticklabels()
    plt.yticks( np.arange(9) , ('','North_AmsMLXe4_CHI','North_ChiMLXe4_AMS','North_ChiMLXe4_TPE','North_TpeMLXe8_CHI',
        'South_AmsMLXe4_CHI','South_ChiMLXe4_AMS','South_ChiMLXe4_TPE','South_TpeMLXe8_CHI'))
    fig.autofmt_xdate()
    plt.xlabel('Date:{0}'.format(datestr))
    plt.title(msg)
    fpath = os.path.join(os.getcwd(),'Flapping{0}.png'.format(datestr))

    # mark duration
    durationXY = []
    resolution = 86400/180. # most have 180 marker
    for index, row in bigdf.query('interval > {0} or interval < 0.0'.format(resolution)).iterrows():
        durationXY.append([row['duration'],row['startdate'] , dicNumb[row['route']]])
        if row['duration'] > 0:
            posx1 = datestr2num(str(row['startdate']))
            posx2 = datestr2num(str(row['enddate']))
            plt.plot([posx1,posx1],[0,dicNumb[row['route']]],'k-',color='red',lw=1.0,alpha=0.7)
            plt.plot([posx2,posx2],[0,dicNumb[row['route']]],'k-',color='red',lw=1.0,alpha=0.7)
            plt.plot([posx1,posx2],[dicNumb[row['route']],dicNumb[row['route']]],'k-',color='red',lw=1.0,alpha=0.7)
        elif row['duration'] == 0:
            posx = datestr2num(str(row['startdate']))
            plt.plot([posx,posx],[0,dicNumb[row['route']]],'k-',color='blue',lw=1.0,alpha=0.7)
    for item in durationXY:
        plt.text(item[1],item[2],'{0}'.format(item[0]),ha='left',va='bottom',rotation=90,fontsize=10)
    plt.savefig(fpath)
    plt.clf()
    #ax.plot_datek(dateseq, y*y)
    boardax = [None] * 8
    fig, ax = plt.subplots(figsize=(12,9))
    plt.clf()
    subdf = bigdf[['duration','route']]
    subdf['count'] = 1
    group1 = subdf.groupby(['duration','route']).count().unstack()
    group1.columns =  group1.columns.droplevel(0)
    i = 0
    themax = bigdf['duration'].value_counts().sort_values(ascending=False).max()
    for item in group1.columns:
        i+=1
        base = 240
        if len(group1.columns) == 1:
            base = 110
        elif len(group1.columns) <= 2:
            base = 120
        elif len(group1.columns) <= 4:
            base = 220
        elif len(group1.columns) <= 8:
            base = 240
        boardax[i-1] = fig.add_subplot(base+i)
        #boardax[i-1] = plt.axes([0.10,0.10,0.78,0.75])
        colors = []
        for ind,it in group1[item].iteritems():
            if str(ind) == '0.0' and not np.isnan(it):
                colors.append('blue')
            elif not np.isnan(it):
                colors.append('red')
        #if not 'red' in colors:
        #    colors = 'blue'

        group1[item].dropna().plot(kind='bar',ax=boardax[i-1],color=colors)
        boardax[i-1].set_xlabel('duration(s)')
        boardax[i-1].set_title(item)
        boardax[i-1].set_ylim(0,themax)
        #boardax[i-1].get_

    #outSer = subdf.groupby('route')['duration']
    #themax = outSer.max()
    #outSer.plot(kind='hist',ax=ax,alpha= 0.6)
    plt.tight_layout()
    fpath = os.path.join(os.getcwd(),'Flapping{0}_duration_hist.png'.format(datestr))
    plt.savefig(fpath)
    plt.clf()

def exe(df,bigdf,refTime,filestring,start_sec= 0,end_sec= 0,number = 86400,subZoom=[]):
    print bigdf.columns
    querystr = 'index > 0'
    additionstr = ''
    if start_sec > 0.1 and end_sec-start_sec < 86200:
        additionstr = '_%.0f_%.0f'%(start_sec-10,end_sec+10)

    msg = 'From {0} to {1}\n'.format(time.ctime(start_sec) , time.ctime(end_sec) )
    start_sec -= refTime
    end_sec -= refTime
    dicRoute = {
            'NorthRoute_AMS_CHI_AmsMLXe4' : 'North_AmsMLXe4_CHI' ,
            'NorthRoute_CHI_AMS_ChiMLXe4' : 'North_ChiMLXe4_AMS' ,
            'NorthRoute_CHI_TPE_ChiMLXe4' : 'North_ChiMLXe4_TPE' ,
            'NorthRoute_TPE_CHI_TpeMLXe8' : 'North_TpeMLXe8_CHI' ,
            'SouthRoute_AMS_CHI_AmsMLXe4' : 'South_AmsMLXe4_CHI' ,
            'SouthRoute_CHI_AMS_ChiMLXe4' : 'South_ChiMLXe4_AMS' ,
            'SouthRoute_CHI_TPE_ChiMLXe4' : 'South_ChiMLXe4_TPE' ,
            'SouthRoute_TPE_CHI_TpeMLXe8' : 'South_TpeMLXe8_CHI' }
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
    if len(subdf) == 0:
            print 'nothing to plot'
            plt.figure(1, figsize=(12,9))
            ax = plt.axes([0.20,0.05,0.78,0.75])
            plt.title('No flapping events today')
            fpath = os.path.join(os.getcwd(),'Flapping{0}.png'.format(filestring+additionstr))
            plt.savefig(fpath)
            plt.clf()
            return
    subdf['refTimeStart'] = subdf['startT_sec'] - refTime
    subdf['refTimeEnd']   = subdf['endT_sec'] - refTime
    #For plot duration label:
    durationXY = []
    resolution = (end_sec-start_sec)/180. # most have 180 marker
    for index, row in subdf.query('interval > {0} or interval < 0.0'.format(resolution)).iterrows():
        if row['refTimeStart'] > 0:
            durationXY.append([row['duration'],row['refTimeStart'] , dicNumb[row['route']]])
        else:
            durationXY.append([row['duration'],row['refTimeEnd'] , dicNumb[row['route']]])
    #print durationXY

    subdf['refTimeStart'].astype(np.int64)
    subdf['refTimeEnd'].astype(np.int64)
    group = pd.groupby(subdf, [subdf.route])
    for index,item in group.count()['endT'].iteritems():
        msg += '{0}: {1} flappings\n'.format(dicRoute[index],item)
    if start_sec > 0.1:
        querystr = 'index > {0} and index < {1}'.format(start_sec-10,end_sec+100)
    for index ,row in subdf.iterrows():
        iStart = int(row['refTimeStart'])
        if row['refTimeStart'] < 0:
            iStart = 0
        df[row['route']].iloc[iStart:int(row['refTimeEnd'])+1] =  dicNumb[row['route']]
    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.20,0.05,0.78,0.75])
    print 'ctime = {0}'.format(time.ctime(refTime))
    df['timeIndex'] = pd.date_range(time.ctime(refTime),periods = number, freq='s')
    timetick = pd.date_range(time.ctime(refTime+50), periods = 9 , freq = '3H')
    timeticklabel = []
    for item in timetick:
        print item , type(item)
        timeticklabel.append('{0}:{1:0>2d}'.format(item.hour,item.minute))
    print 'lendf for draw =' , len(df[['timeIndex','SouthRoute_AMS_CHI_AmsMLXe4','SouthRoute_CHI_AMS_ChiMLXe4','SouthRoute_CHI_TPE_ChiMLXe4','SouthRoute_TPE_CHI_TpeMLXe8']].query(querystr))
    listDFindex = ['timeIndex','SouthRoute_AMS_CHI_AmsMLXe4', 'SouthRoute_CHI_AMS_ChiMLXe4',
                               'SouthRoute_CHI_TPE_ChiMLXe4', 'SouthRoute_TPE_CHI_TpeMLXe8',
                               'NorthRoute_AMS_CHI_AmsMLXe4', 'NorthRoute_CHI_AMS_ChiMLXe4',
                               'NorthRoute_CHI_TPE_ChiMLXe4', 'NorthRoute_TPE_CHI_TpeMLXe8' ]
    #ax = df[listDFindex].query(querystr).plot(kind='line',x = 'timeIndex', marker='o',markersize=1,color='blue',
    if (end_sec-start_sec >= 86200):
        df[listDFindex].plot(kind='line', marker='o',markersize=1,color='blue',ax = ax,
                figsize=(12,9),ylim=(0,8.2), alpha = 0.5, legend=False)
        #df[listDFindex].query('duration>0').plot(kind='line', marker='o',markersize=1,color='blue',ax = ax,
        #        figsize=(12,9),ylim=(0,8.2), alpha = 0.5, legend=False)
        plt.xticks(np.arange(50,86700,10800),tuple(timeticklabel))
    else:
        df[listDFindex].query(querystr).plot(kind='line',x= 'timeIndex', marker='o',markersize=1,color='blue',ax = ax,
                figsize=(12,9),ylim=(0,8.2), alpha = 0.5, legend=False)

    plt.yticks( np.arange(9) , ('','North_AmsMLXe4_CHI','North_ChiMLXe4_AMS','North_ChiMLXe4_TPE','North_TpeMLXe8_CHI',
        'South_AmsMLXe4_CHI','South_ChiMLXe4_AMS','South_ChiMLXe4_TPE','South_TpeMLXe8_CHI'))
    plt.xlabel('Date:{0}'.format(filestring))
    plt.title(msg)

    for item in durationXY:
        if (end_sec-start_sec <= 86200):
            plt.text(df['timeIndex'][int(item[1])],item[2],'{0}'.format(item[0]),ha='left',va='bottom',rotation=90,fontsize=10)
            print 'case1'
        else:
            plt.text(item[1],item[2],'{0}'.format(item[0]),ha='left',va='bottom',rotation=90,fontsize=10)
            print 'case2'
        #markduration(item)

    fpath = os.path.join(os.getcwd(),'Flapping{0}.png'.format(filestring+additionstr))
    plt.savefig(fpath)
    # leave a copy
    if (end_sec-start_sec <= 86200):
        fpath = os.path.join(os.getcwd(),'Flapping{0}.png'.format(filestring+additionstr))
        plt.savefig(fpath)
    plt.clf()

    print fpath
    if (end_sec-start_sec <= 86200):
        return

    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.20,0.15,0.78,0.75])
    #import matplotlib
    #matplotlib.style.use('ggplot')
    subdf = subdf[['duration','route']]
    subdf['count'] = 1
    group1 = subdf.groupby(['duration','route']).count().unstack()
    print group1
    group1.columns =  group1.columns.droplevel(0)
    print group1
    group1.plot(kind='bar', edgecolor='none',stacked=True)
    #outSer = subdf.groupby('route')['duration']
    #themax = outSer.max()
    #outSer.plot(kind='hist',ax=ax,alpha= 0.6)
    plt.xlabel('Duration (sec)')
    plt.ylabel('counts')
    fpath = os.path.join(os.getcwd(),'Flapping{0}_duration_hist.png'.format(filestring+additionstr))
    plt.savefig(fpath)
    plt.clf()
    return

def getDays(seconds):
    import datetime
    MM = time.gmtime(seconds)[1]
    DD = time.gmtime(seconds)[2]
    print (datetime.datetime(2017,MM,DD)-datetime.datetime(2017,1,1)).days
    return (datetime.datetime(2017,MM,DD)-datetime.datetime(2017,1,1)).days
    
def drawDowntimeEventsToday(bigdf):
    yesterday = time.mktime(time.strptime(timeModule.getYesterday(),'%Y%m%d'))
    yesterday_sec = yesterday 
    drawDowntimeEvents(bigdf,yesterday_sec,yesterday_sec+86400)

def drawDowntimeEvents(bigdf,start_sec,end_sec):
    #number = 86400
    number = 86400+3600
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
    ser = pd.date_range('1/1/2017' ,periods = 365, freq='D')
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
    print bigdf.head()
    #exe(df ... is legasi, will not be used and maintained seriously
    #exe(df,bigdf,start_sec-50,datestr,start_sec,end_sec,number)
    exe2(bigdf,datestr)

#csvlist = [
#'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
#'SouthRoute_TPE_CHI_TpeMLXe8.csv'
#]
csvlist = [
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe8.csv' ,
'SouthRoute_CHI_AMS_ChiMLXe4.csv' ,
'SouthRoute_AMS_CHI_AmsMLXe4.csv' ,
'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
'NorthRoute_CHI_AMS_ChiMLXe4.csv' ,
'NorthRoute_AMS_CHI_AmsMLXe4.csv'
]

dflist = []
for i in csvlist:
    dflist.append( function_df.getDF_netlog(i) )

newdf = function_df.getDF_netlog_total( dflist ).sort()

drawDowntimeEventsToday(newdf)

#intervals = ana_FlappingBlocks.exefunc(newdf)
#for item in intervals:
#    drawDowntimeEvents(newdf,item[0],item[1])


#timelist = ana_FlappingBlocks2.exefunc(newdf)
#for item in timelist:
#    drawDowntimeEvents(newdf, item[0], item[1])
