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
import datetime
import timeModule
import ana_FlappingBlocks
from matplotlib.ticker import NullFormatter
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def getDays(seconds):
    import datetime
    MM = time.gmtime(seconds)[1]
    DD = time.gmtime(seconds)[2]
    print (datetime.datetime(2016,MM,DD)-datetime.datetime(2016,1,1)).days
    return (datetime.datetime(2016,MM,DD)-datetime.datetime(2016,1,1)).days
    
def draw2(powerdf,bigdf,route,start_sec = -1,end_sec = -1):
    #print 'debug:powerdf before query =', len(powerdf)
    queryString = 'route=="{0}" and endT_sec > {1} and startT_sec < {2}'.format(route,powerdf['abstime'][0],powerdf['abstime'][-1])
    if start_sec > 0:
        queryString = 'route=="{0}" and endT_sec > {1} and startT_sec < {2}'.format(route,start_sec,end_sec)
        powerdf = powerdf.query('abstime>= {0} and abstime<{1}'.format(start_sec,end_sec))
    else:
        queryTime = timeModule.getUnixDaySecond(powerdf.abstime[-5])
        print time.ctime(queryTime), powerdf.abstime[-1]
        powerdf = powerdf.query('abstime>= {0} and abstime<{1}'.format(queryTime,queryTime+86400))
        #print 'lines after query = ' , len( powerdf)

    subdf = bigdf.query(queryString)
    #subdf = bigdf

    #start to draw
    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.20,0.15,0.78,0.75])
    powerdf['Tx'].plot(kind='line',ax=ax,color='b',legend=True,alpha=0.8,ylim=(-21,3.5))
    powerdf['Rx'].plot(kind='line',ax=ax,color='r',legend=True,alpha=0.8,ylim=(-21,3.5))
    # draw threshold
    print 'checkTime (abs)',powerdf['abstime'][-1]
    startdate = datetime.datetime.fromtimestamp(powerdf['abstime'][0])
    if (start_sec > 0.5):
        startdate = datetime.datetime.fromtimestamp(powerdf['abstime'][0])

    linestart = mdates.date2num(datetime.datetime.fromtimestamp(powerdf['abstime'][0]))
    lineend = mdates.date2num(datetime.datetime.fromtimestamp(powerdf['abstime'][-1]))
    plt.plot([linestart,lineend],[2.5,2.5],'k--',color='red',alpha=0.7)
    plt.plot([linestart,lineend],[2.0,2.0],'k--',color='blue',alpha=0.7)
    plt.plot([linestart,lineend],[-20.0,-20.0],'k--',color='red',alpha=0.7)
    plt.plot([linestart,lineend],[-7.9997,-7.9997],'k--',color='blue',alpha=0.7)
    plt.text(linestart,2.5,'Rx Upper Threshold',color='red',alpha=0.7)
    plt.text(linestart,2.0,'Tx Upper Threshold',color='blue',alpha=0.7)
    plt.text(linestart,-20.0,'Rx Lower Threshold',color='red',alpha=0.7)
    plt.text(linestart,-7.9997, 'Tx Lower Threshold',color='blue',alpha=0.7)

    #draw shadow:
    rec_bottom = ax.get_ylim()[0]
    rec_height = ax.get_ylim()[1]
    trans = transforms.blended_transform_factory(
                ax.transData, ax.transAxes)
    rects = []
    dictRoute = {
            'NorthRoute_CHI_TPE_ChiMLXe4' : 'North_ChiMLXe4',
            'NorthRoute_TPE_CHI_TpeMLXe8' : 'North_TpeMLXe8',
            'SouthRoute_CHI_TPE_ChiMLXe4' : 'South_ChiMLXe4',
            'SouthRoute_TPE_CHI_TpeMLXe8' : 'South_TpeMLXe8'
            }
    for index,row in subdf.iterrows():
        start = mdates.date2num(datetime.datetime.fromtimestamp(row['startT_sec']))
        end = mdates.date2num(datetime.datetime.fromtimestamp(row['endT_sec']))
        rect =  patches.Rectangle((start,rec_bottom), width=(end-start), height=rec_height+20,
                color='orange', alpha=0.5)
        ax.add_patch(rect)
    orange_patch = mpatches.Patch(color='orange', label='Flapping time')
    blueline = mlines.Line2D([], [], color='blue', label='Tx')
    redline = mlines.Line2D([], [], color='red', label='Rx')
    plt.legend(handles=[orange_patch,blueline,redline])
    
    plt.ylabel('dBm')
    plt.xlabel('Date:{0}{1:0>2d}{2:0>2d}'.format(startdate.year,startdate.month,startdate.day))
    plt.title(dictRoute[route])
    if (start_sec>0):
        plt.savefig('power_{0}_{1}_{2}_{3}.png'.format(dictRoute[route],timeModule.getYesterday(),start_sec,end_sec))
    else:
        plt.savefig('power_{0}_{1}.png'.format(dictRoute[route],timeModule.getYesterday()))
    plt.clf()

    #Plot total
    if (start_sec < 0):
        plt.figure(1, figsize=(12,9))
        ax = plt.axes([0.20,0.15,0.78,0.75])
        yButtom = np.minimum(powerdf['Tx'].min(),powerdf['Rx'].min()) - 15
        powerdf['Tx'].plot(kind='line',ax=ax,color='b',ylim=(yButtom,10))
        powerdf['Rx'].plot(kind='line',ax=ax,color='r',ylim=(yButtom,10))
        # draw threshold
        print 'checkTime (abs)',powerdf['abstime'][-1]
        startdate = datetime.datetime.fromtimestamp(powerdf['abstime'][0])

        #draw shadow:
        rec_bottom = ax.get_ylim()[0]
        rec_height = ax.get_ylim()[1]
        linestart = mdates.date2num(datetime.datetime.fromtimestamp(powerdf['abstime'][0]))
        lineend = mdates.date2num(datetime.datetime.fromtimestamp(powerdf['abstime'][-1]))
        plt.plot([linestart,lineend],[0.5,0.5],'k--',color='red',alpha=0.7)
        plt.plot([linestart,lineend],[-14.2,-14.2],'k--',color='red',alpha=0.7)
        plt.plot([linestart,lineend],[-8.2,-8.2],'k--',color='blue',alpha=0.7)
        plt.text(linestart,0.5,'Rx,Tx Upper Threshold',color='black',alpha=0.7)
        plt.text(linestart,-14.2,'Rx Lower Threshold',color='red',alpha=0.7)
        plt.text(linestart,-8.2, 'Tx Lower Threshold',color='blue',alpha=0.7)
        for index,row in subdf.iterrows():
            start = mdates.date2num(datetime.datetime.fromtimestamp(row['startT_sec']))
            end = mdates.date2num(datetime.datetime.fromtimestamp(row['endT_sec']))
            rect =  patches.Rectangle((start,rec_bottom), width=(end-start), height=rec_height+20,
                    color='orange', alpha=0.5)
            ax.add_patch(rect)
        orange_patch = mpatches.Patch(color='orange', label='Flapping time')
        blueline = mlines.Line2D([], [], color='blue', label='Tx')
        redline = mlines.Line2D([], [], color='red', label='Rx')
        plt.legend(handles=[orange_patch,blueline,redline])
        plt.ylabel('dBm')
        plt.xlabel('Date:{0}{1:0>2d}{2:0>2d}'.format(startdate.year,startdate.month,startdate.day))
        plt.title(dictRoute[route])
        plt.savefig('power_{0}_{1}_fullrange.png'.format(dictRoute[route],timeModule.getYesterday()))
        plt.clf()



csvlist = [
'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'NorthRoute_TPE_CHI_TpeMLXe8.csv',
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe8.csv'
]

dflist = []
for i in csvlist:
    dflist.append( function_df.getDF_netlog(i) )

newdf = function_df.getDF_netlog_total( dflist ).sort()

pcsvlist = [
        'data_CHIBR0_Optical_20160809.csv',
        'data_TWBR2_Optical_20160809.csv'
        ]

# Draw North_TWBR2
pdf = pd.read_csv('data_North_TWBR2_Optical.csv',index_col='date',parse_dates=True)
draw2(pdf,newdf,'NorthRoute_TPE_CHI_TpeMLXe8')
intervals = ana_FlappingBlocks.exefunc(newdf.query('route=="NorthRoute_TPE_CHI_TpeMLXe8"'))

# Draw North_CHIBR0
pdf = pd.read_csv('data_North_CHIBR0_Optical.csv',index_col='date',parse_dates=True)
draw2(pdf,newdf,'NorthRoute_CHI_TPE_ChiMLXe4')

# Draw South_TWBR2
pdf = pd.read_csv('data_South_TWBR2_Optical.csv',index_col='date',parse_dates=True)
draw2(pdf,newdf,'SouthRoute_TPE_CHI_TpeMLXe8')
intervals = ana_FlappingBlocks.exefunc(newdf.query('route=="SouthRoute_TPE_CHI_TpeMLXe8"'))
for item in intervals:
    print 'SouthRoute_TPE_CHI_TpeMLXe8' , item[0]-50,item[1]+50
    draw2(pdf,newdf,'SouthRoute_TPE_CHI_TpeMLXe8',item[0]-50,item[1]+50)

# Draw South_CHIBR0
pdf = pd.read_csv('data_South_CHIBR0_Optical.csv',index_col='date',parse_dates=True)
draw2(pdf,newdf,'SouthRoute_CHI_TPE_ChiMLXe4')
intervals = ana_FlappingBlocks.exefunc(newdf.query('route=="SouthRoute_CHI_TPE_ChiMLXe4"'))
for item in intervals:
    print 'SouthRoute_CHI_TPE_ChiMLXe4' , item[0]-50,item[1]+50
    draw2(pdf,newdf,'SouthRoute_CHI_TPE_ChiMLXe4',item[0]-50,item[1]+50)

