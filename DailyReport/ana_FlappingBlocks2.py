import os
import function_df
import pandas as pd
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
    previous = 0
    previndex = None
    group = []
    startG, endG = None, None
    flag_continue = False
    groupCounts = 0
    timearray = np.array([])
    for index, row in bigdf.iterrows():
        timearray = np.append(timearray,row['startT_sec'])
        timearray = np.append(timearray,row['endT_sec'])
    timearray = np.sort(timearray)
    count = 0
    groups = []
    output = []
    for item in timearray:
        if (item - previous) < 0:
            print 'Problem!!', item, previous
        previous = item
        if len(groups) == 0:
            groups.append(item)
            continue
        elif len(groups) > 0 and (item-groups[-1]) > 300:
            if len(groups) > 10:
                output.append([groups[0],groups[-1]])
                #print groups[0],groups[-1],groups[-1]-groups[0],len(groups)
            groups = [item]
            continue
        elif len(groups) > 0 and  (item-groups[-1]) <= 300:
            groups.append(item)
            continue
        else:
            print 'something strange happened!!!'
    if len(groups)> 10:
        output.append([groups[0],groups[-1]])
    return output



#csvlist = [
#'NorthRoute_AMS_CHI_AmsMLXe4.csv' ,
#'NorthRoute_CHI_AMS_ChiMLXe4.csv' ,
#'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
#'NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
#'SouthRoute_AMS_CHI_AmsMLXe4.csv' ,
#'SouthRoute_CHI_AMS_ChiMLXe4.csv' ,
#'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
#'SouthRoute_TPE_CHI_TpeMLXe8.csv'
#]
##
#dflist = []
#for i in csvlist:
#    dflist.append( function_df.getDF_netlog(i) )
#
#newdf = function_df.getDF_netlog_total( dflist ).sort_values(by='startT_sec')
#
#exefunc(newdf)

#for item in exefunc(newdf):
#    print '[{0},{1}],'.format(item[0],item[1])
