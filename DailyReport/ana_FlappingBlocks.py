import os
import matplotlib
matplotlib.use('Agg')
import sys
sys.path.append('../../NetworkDev')
import function_df
import pandas as pd
import pylab as plt
import numpy as np
import time

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
                    print 'From' , startG , 'to', endG, 'duration',endG-startG, 'Groups = ' , groupCounts
                    print 'From' , time.ctime(startG) , 'to' , time.ctime(endG), 'Groups = ' , groupCounts
                    group.append([startG,endG])
                groupCounts = 0
                flag_continue = False
            # last one    
            elif index == bigdf.index[-1] and groupCounts > 1:
                #print index
                #print row
                #print 'theend'
                print 'From' , time.ctime(startG) , 'to' , time.ctime(endG), 'Groups = ' , groupCounts
                break
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
    print group
    return group
        #return group


#csvlist = [
#'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
#'SouthRoute_TPE_CHI_TpeMLXe8.csv'
#]
#
#dflist = []
#for i in csvlist:
#    dflist.append( function_df.getDF_netlog(i) )
#
#newdf = function_df.getDF_netlog_total( dflist ).sort_values(by='startT_sec')
#
#exefunc(newdf)
