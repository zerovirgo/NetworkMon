# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 07:29:11 2016

@author: kschen
"""

import pandas as pd
import numpy as np
import pylab as plt
import function_df
from matplotlib.ticker import NullFormatter


def drawDownTimeVSInterval(filename):
    title = filename.split('.')[0]+' flapping duration v.s. interval'
    outname = filename.split('.')[0]+'fDuration_vs_fInterval'+'.png'
    df = function_df.getDF_netlog(filename)
    #print df.head()
    nullfmt = NullFormatter()         # no labels

    # definitions for the axes
    left, width = 0.1, 0.55
    bottom, height = 0.1, 0.55
    bottom_h = left_h = left + width + 0.02

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.3]
    rect_histy = [left_h, bottom, 0.3, height]

    # start with a rectangular Figure
    plt.figure(1, figsize=(12, 12))

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)

    # the scatter plot:
    axScatter.scatter(df['duration'], df['interval'])
    
    # now determine nice limits by hand:
    binwidth = 10
    xymax = np.max([np.max(np.fabs(df['duration'])), np.max(np.fabs(df['interval']))])
    xymax = 500
    lim = (int(xymax/binwidth) + 1) * binwidth

    axScatter.set_xlim((-10, 1000))
    axScatter.set_ylim((-10, 1000))

    bins = np.arange(-10, 1000 + binwidth, binwidth)
    axHistx.hist(df['duration'], bins=bins)
    axHisty.hist(df['interval'], bins=bins, orientation='horizontal')
    
    axHistx.set_title(title)
    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())
    axScatter.set_xlabel('Flapping duration (sec)')
    axScatter.set_ylabel('Interval between flappings (sec)')
    #plt.show()
    plt.savefig(outname)
    plt.clf()
    return

def drawDownTimeStatDay(filename,limit = False):
    n = 3
    #only difference betwrrn day and week...
    df = function_df.dfGroupByDay(function_df.getDF_netlog(filename))
    title = filename.split('.')[0]+' average flapping duration\n'
    title += 'From {0} to {1} got {2} days with flapping (Total = {3} min)'.format(df.index[0]
            ,df.index[-1],len(df['count']),df['count'].sum()/60.)
    outname = filename.split('.')[0]+'_avg_flp_dur_day'+'.png'
    # are ablve lines
    ax = plt.axes([0.15,0.25,0.8,0.65])
    if limit:
        outname = filename.split('.')[0]+'_avg_flp_dur_day_zoom'+'.png'
        ax = df['duration'].plot(kind='bar',alpha=0.7,figsize=(12,7),ylim=(0,3600))
    else:
        ax = df['duration'].plot(kind='bar',alpha=0.7,figsize=(12,7))
    #if len(df > 100):
    #    ticks = ax.xaxis.get_ticklocs()
    #    ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
    #    ax.xaxis.set_ticks(ticks[::n])
    #    ax.xaxis.set_ticklabels(ticklabels[::n])
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Average flapping duration/day(sec)')
    plt.savefig(outname)
    plt.clf()

    #title = filename.split('.')[0]+' average interval between flappings'
    #outname = filename.split('.')[0]+'_avg_flp_itv_day'+'.png'
    #ax = plt.axes([0.15,0.25,0.8,0.65])
    #if limit:
    #    outname = filename.split('.')[0]+'_avg_flp_itv_day_zoom'+'.png'
    #    ax = df['interval'].plot(kind='bar',alpha=0.7,figsize=(12,7),ylim=(0,3600))
    #else:
    #    ax = df['interval'].plot(kind='bar',alpha=0.7,figsize=(12,7))

    #if len(df > 100):
    #    ticks = ax.xaxis.get_ticklocs()
    #    ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
    #    ax.xaxis.set_ticks(ticks[::n])
    #    ax.xaxis.set_ticklabels(ticklabels[::n])
    #ax.set_title(title)
    #ax.set_xlabel('Date')
    #ax.set_ylabel('Average interval between flappings/day (sec)')
    #ax = plt.axes([0.15,0.25,0.8,0.65])
    #plt.savefig(outname)
    #plt.clf()
    #if limit:
    #    return

    title = filename.split('.')[0]+' flapping per day\n'
    title += 'From {0} to {1} got {2} days with flapping (Total = {3})'.format(df.index[0]
            ,df.index[-1],len(df['count']),df['count'].sum())
    print title
    print df.describe()
    outname = filename.split('.')[0]+'_count_flp_day'+'.png'
    ax = plt.axes([0.15,0.25,0.8,0.65])
    ax = df['count'].plot(kind='bar',alpha=0.7,figsize=(16,7))
    # skip information
    #if len(df > 100):
    #    ticks = ax.xaxis.get_ticklocs()
    #    ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
    #    ax.xaxis.set_ticks(ticks[::n])
    #    ax.xaxis.set_ticklabels(ticklabels[::n])
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('counts')
    plt.savefig(outname)
    plt.clf()

    return


def drawDownTimeStatWeek(filename):
    n = 3
    #only difference betwrrn day and week...
    df = function_df.dfGroupByDay(function_df.getDF_netlog(filename))
    title = filename.split('.')[0]+' average flapping duration'
    title += 'From {0} to {1} got {2} days with flapping (Total = {3} min)'.format(df.index[0]
            ,df.index[-1],len(df['count']),df['count'].sum()/60.)
    outname = filename.split('.')[0]+'_avg_flp_dur_week'+'.png'
    # are ablve lines
    ax = plt.axes([0.12,0.25,0.8,0.65])
    ax = df['duration'].plot(kind='bar',alpha=0.7,figsize=(12,7))
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Average flapping duration/day(sec)')
    if len(df > 100):
        ticks = ax.xaxis.get_ticklocs()
        ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
        ax.xaxis.set_ticks(ticks[::n])
        ax.xaxis.set_ticklabels(ticklabels[::n])
    plt.savefig(outname)
    plt.clf()

    #title = filename.split('.')[0]+' average interval between flappings'
    #outname = filename.split('.')[0]+'_avg_flp_itv_week'+'.png'
    #ax = plt.axes([0.15,0.25,0.8,0.65])
    #ax = df['interval'].plot(kind='bar',alpha=0.7,figsize=(12,7))
    #ax.set_title(title)
    #ax.set_xlabel('Date')
    #ax.set_ylabel('Average interval between flappings/day (sec)')
    #if len(df > 100):
    #    ticks = ax.xaxis.get_ticklocs()
    #    ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
    #    ax.xaxis.set_ticks(ticks[::n])
    #    ax.xaxis.set_ticklabels(ticklabels[::n])
    #plt.savefig(outname)
    #plt.clf()

    title = filename.split('.')[0]+' flapping per day\n'
    title += 'From {0} to {1} got {2} days with flapping (Total = {3})'.format(df.index[0]
            ,df.index[-1],len(df['count']),df['count'].sum())
    print title
    outname = filename.split('.')[0]+'_count_flp_week'+'.png'
    ax = plt.axes([0.12,0.25,0.8,0.65])
    ax = df['count'].plot(kind='bar',alpha=0.7,figsize=(12,7))
    if len(df) > 100:
        ticks = ax.xaxis.get_ticklocs()
        ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
        ax.xaxis.set_ticks(ticks[::n])
        ax.xaxis.set_ticklabels(ticklabels[::n])
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('counts')
    plt.savefig(outname)
    plt.clf()

    return

def compareCount():
    filename1 = 'SouthRoute_CHI_TPE_ChiMLXe4.csv'
    filename2 = 'SouthRoute_TPE_CHI_TpeMLXe4.csv'
    title = 'Network flapping per day'
    outname = 'comp_TPE2CHI_vs_CHI_TPE_count_flp_day'+'.png'
    df1 = function_df.dfGroupByDay(function_df.getDF_netlog(filename1))
    df2 = function_df.dfGroupByDay(function_df.getDF_netlog(filename2))

    ax = plt.axes([0.15,0.25,0.8,0.65])
    ax = df1['count'].plot(kind='line',figsize=(12,7),alpha=0.5,color = 'r',label='South CHI to TPE')
    df2['count'].plot(kind='line',alpha=0.5,ax = ax, color='b',label='South CHI to TPE')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('counts')
    plt.savefig(outname)
    plt.clf()
    print 'Down'
    return


def modax(ax):
    n = 3
    ticks = ax.xaxis.get_ticklocs()
    ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
    ax.xaxis.set_ticks(ticks[::n])
    ax.xaxis.set_ticklabels(ticklabels[::n])

# not finished yet
def drawDownTimeStat(filename):
    title = filename.split('.')[0]+' flapping per day'
    outname = filename.split('.')[0]+'_count_flp_week'+'.png'
    df = function_df.getDF_netlog(filename)
    ax = df['duration'].plot(kind='hist',xlim=(0,10))


myname = 'NorthRoute_CHI_TPE_ChiMLXe4.csv'
drawDownTimeVSInterval(myname)
drawDownTimeStatDay(myname)

myname = 'NorthRoute_TPE_CHI_TpeMLXe8.csv'
drawDownTimeVSInterval(myname)
drawDownTimeStatDay(myname)

myname = 'SouthRoute_CHI_TPE_ChiMLXe4.csv'
drawDownTimeVSInterval(myname)
drawDownTimeStatDay(myname)
#drawDownTimeStatWeek(myname)

myname = 'SouthRoute_TPE_CHI_TpeMLXe8.csv'
drawDownTimeVSInterval(myname)
drawDownTimeStatDay(myname)
#drawDownTimeStatWeek(myname)
#compareCount()

    #rect_scatter =
    #ax = df.plot(kind = 'scatter',x= 'duration', y = 'interval',xlim=(-10,1000),ylim=(-10,1000),figsize=(12,9))
    #plt.title(title)
    #plt.xlabel('Flapping duration (sec)')
    #plt.ylabel('Interval between flappings (sec)')
    #ax2 = df.plot(kind = 'scatter',x= 'duration', y = 'interval')
    #plt.title(title)
    #plt.xlabel('Flapping duration (sec)')
    #plt.ylabel('Interval between flappings (sec)')
    
    
