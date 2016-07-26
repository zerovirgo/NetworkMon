import os
import matplotlib
matplotlib.use('Agg')
import function_df
import pandas as pd
import pylab as plt
import numpy as np
import time

#def GetGroupInterval(group):
#    groupStart = 0
#    groupEnd = 0
#    if len(group)!=0:
#        groupStart = group[0]['starT_sec']
#        groupEnd   = group[0]['endT_sec']
#        for i in range(1,len(group)):
#            if groupEnd < group[i]['endT_sec']
#            groupEnd = group[i]['endT_sec']

def exefunc(bigdf):
    infosets = []
    previous = None
    previndex = None
    group = []
    startG, endG = None, None
    flag_continue = False
    groupCounts = 0
    for index, row in bigdf.iterrows():
        if previous is None:
            print 'empty'
            previous = row
            previndex = index
            continue
        if groupCounts != 0:
            if row['startT_sec'] - endG > 300:
                if groupCounts > 1:
                    #print 'From' , startG , 'to', endG, 'Groups = ' , groupCounts
                    print 'From' , time.ctime(startG) , 'to' , time.ctime(endG), 'Groups = ' , groupCounts
                    group.append([startG,endG])
                groupCounts = 0
                flag_continue = False
            # last one    
            elif index == bigdf.index[-1] and groupCounts > 1:
                    print 'From' , time.ctime(startG) , 'to' , time.ctime(endG), 'Groups = ' , groupCounts
            else:
                if( row['endT_sec'] - endG) >= 0:
                    endG = row['endT_sec']
                #else:
                #    print 'wired:From' , time.ctime(row['endT_sec']) , 'to' , time.ctime(endG), 'Groups = ' , groupCounts, row['endT_sec'] - endG
                groupCounts += 1
                #print 'From' , startG , 'to', endG, 'Groups = ' , groupCounts

        if groupCounts == 0:
            startG, endG = previous['startT_sec'],previous['endT_sec']
            groupCounts += 1
        previous = row
        previndex = index
        #return group


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

newdf = function_df.getDF_netlog_total( dflist ).sort('startT_sec')

exefunc(newdf)
