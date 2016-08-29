import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as plt
import time
import timeModule


def getInterval(df,startLoc,endLoc):
    #print 'getInter df range, inputrange', df['abstime'][df.index[0]], df['abstime'][df.index[-1]], startLoc,endLoc
    #print 'getInter df range, inputrange', df['abstime'][df.index[0]]<=startLoc, df['abstime'][df.index[-1]]>= endLoc
    subdf = df.query('abstime > {0} and abstime < {1}'.format(startLoc,endLoc))
    subdff = df.query('abstime <= {0}'.format(startLoc))
    subdfff = df.query('abstime >= {0}'.format(endLoc))
    indBefore, indStart, indEnd, indAfter = None, None, None, None
    if len(subdf) > 0:
        indStart, indEnd = subdf.index[0], subdf.index[-1]
    if len(subdff) > 0:
        indBefore = subdff.index[-1]
    if len(subdff) > 0:
        indAfter = subdfff.index[0]
    return indBefore, indStart, indEnd, indAfter

def exeDataPross(csvpower,csvflapping,route):
    print route
    nDay = -1
    fout = open('FlappingEventsTable_{0}_{1}.html'.format(route,timeModule.getNday(nDay)),'w')
    dfP =  pd.read_csv(csvpower)
    dfF =  pd.read_csv(csvflapping)
    line = '''
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="Creation-Date" content="test">
<title>HTML Examples</title>
</head>

<body>
    '''
    fout.writelines(line)
    fout.writelines('\n<h2 align=center>Flapping Record {0} {1}</h2>\n'.format(route,timeModule.getNday(nDay)))
    line = '''
<table border=1 bordercolor=#003366 width=500>
    <caption align=left>Table:</caption>
    <tr>
        <th width=15%>Start Time</th>
        <th width=15%>End Time</th>
        <th width=5%>Time before flapping</th>
        <th width=7%>Rx (before)</th>
        <th width=7%>Tx (before)</th>
        <th width=8%>5 min before flapping Rx</th>
        <th width=8%>5 min before flapping Tx</th>
        <th width=5%>Time after flapping</th>
        <th width=7%>Rx (after)</th>
        <th width=7%>Tx (after)</th>
        <th width=8%>5 min after flapping Rx</th>
        <th width=8%>5 min after flapping Tx</th>

    </tr> 
    '''
    fout.writelines(line)

    print 'dfP ' , len(dfP) ,'dfF', len(dfF)
    for index, row in dfF.iterrows():
        iBefore, iStart, iEnd, iAfter = getInterval(dfP,row['startT_sec'],row['endT_sec'])
        # Start fill infomation before flapping
        timeBefore = '--'
        beforeTx = '--'
        beforeRx = '--'
        before5minRx = '--'
        before5minTx = '--'
        if iBefore is not None:
            timeBefore = '{0} sec'.format(dfP.loc[iBefore,'abstime'] - row['startT_sec'])
            beforeRx = '{0:0.3f}'.format(dfP.loc[iBefore,'Rx'] )
            beforeTx = '{0:0.3f}'.format(dfP.loc[iBefore,'Tx'] )
            queryStr = 'abstime > {0} and abstime < {1}'.format(dfP.loc[iBefore,'abstime']-300,dfP.loc[iBefore,'abstime'])
            tempdf = dfP.query(queryStr)
            if len(tempdf)>2:
                ser = tempdf['Rx']
                before5minRx = '{0:0.3f}+-{1:0.3f}'.format(ser.mean(),ser.std())
                ser = tempdf['Tx']
                before5minTx = '{0:0.3f}+-{1:0.3f}'.format(ser.mean(),ser.std())

        #Then After flapping
        timeAfter = '--'
        afterRx = '--'
        afterTx = '--'
        after5minRx = '--'
        after5minTx = '--'
        if iAfter is not None:
            timeAfter = '{0} sec'.format(dfP.loc[iAfter,'abstime'] - row['endT_sec'])
            afterRx = '{0:0.3f}'.format(dfP.loc[iAfter,'Rx'] )
            afterTx = '{0:0.3f}'.format(dfP.loc[iAfter,'Tx'] )
            queryStr = 'abstime > {0} and abstime < {1}'.format(dfP.loc[iAfter,'abstime'],dfP.loc[iAfter,'abstime']+300)
            tempdf = dfP.query(queryStr)
            if len(tempdf)>2:
                ser = tempdf['Rx']
                after5minRx = '{0:0.3f}+-{1:0.3f}'.format(ser.mean(),ser.std())
                ser = tempdf['Tx']
                after5minTx = '{0:0.3f}+-{1:0.3f}'.format(ser.mean(),ser.std())

        print row['startT'], row['endT'], timeBefore , beforeRx , beforeTx , before5minRx , before5minTx , timeAfter , afterRx , afterTx
        infos = [ row['startT'], row['endT'], timeBefore , beforeRx , beforeTx , 
                before5minRx , before5minTx , timeAfter , afterRx , afterTx , after5minRx, after5minTx]
        fout.writelines('<tr>\n')
        for info in infos:
            fout.writelines('<td>{0}</td>\n'.format(info))
        fout.writelines('</tr>\n')
    fout.writelines('</table>\n')
    fout.writelines('</hr>\n')
    fout.writelines('</html>\n')
    fout.close()

mydf = exeDataPross('data_North_CHIBR0_Optical.csv','NorthRoute_CHI_TPE_ChiMLXe4.csv','North_ChiMLXe4')
mydf = exeDataPross('data_North_TWBR2_Optical.csv','NorthRoute_TPE_CHI_TpeMLXe8.csv','North_TpeMLXe8')
mydf = exeDataPross('data_South_CHIBR0_Optical.csv','SouthRoute_CHI_TPE_ChiMLXe4.csv','South_ChiMLXe4')
mydf = exeDataPross('data_South_TWBR2_Optical.csv','SouthRoute_TPE_CHI_TpeMLXe8.csv','South_TpeMLXe8')
