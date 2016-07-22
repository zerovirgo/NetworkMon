# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 00:50:53 2016

@author: kschen
"""

import os
import pandas as pd
import numpy as np

#set your dist:
os.chdir('/home/kschen/anaconda/Projects/NetworkMon/NetworkDev')

def getDF_netlog(fName):
    df = pd.read_csv(fName,index_col='startT',parse_dates=True)
    #df = pd.DataFrame(df, columns=['date_time','startT','endT','route'])
    return df

def dfGroupByDay(df):
    group1 = pd.groupby(df, [df.index.year,df.index.month,df.index.day])
    buffer0 = group1.mean()
    buffer0['count'] = group1.count()['duration']
    indexnames = []
    for i in buffer0.index: # format (month, day, year) -> want to be year/mon/day
        indexnames.append('{0}/{1}/{2}'.format(i[0],i[1],i[2]))
    #print indexnames
    #print type(indexnames[0])
    buffer0 = buffer0.set_index(np.array(indexnames))
    return buffer0

def dfGroupByWeek(df):
    group1 = pd.groupby(df, [df.index.week,df.index.year])
    buffer0 = group1.mean()
    buffer0['count'] = group1.count()['duration']
    indexnames = []
    for i in buffer0.index: # format (month, day, year) -> want to be year/mon/day
        indexnames.append('{0}/{1}/{2}'.format(i[2],i[0],i[1]))
    #print indexnames
    #print type(indexnames[0])
    buffer0 = buffer0.set_index(np.array(indexnames))
    return buffer0

def getDF_netflow(fName):
    foldername = 'FlowData'
    filepath = os.path.join(os.getcwd(),foldername,fName)
    if not os.path.exists(filepath):
        print 'File didnot', filepath ,' exist'
        os.exit()
    df = pd.read_csv(filepath,header=None)
    df.columns = np.array(['date','abstime','input','output'])
    return df

#fname= 'SouthRoute_TPE_CHI_TpeMLXe4.csv'
#mydf = getDF_netlog(fname)
#temp = dfGroupByDay(mydf)
#print mydf.head()
