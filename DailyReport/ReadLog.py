# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 00:06:17 2016

@author: kschen
"""
import time
import timeModule

def getInfoList(filename):
    if '/' in filename:
        return filename.split('/')[-1].split('.')[0].split('_')
    else:
        return filename.split('.')[0].split('.')[0].split('_')

def getCSV(filename,outputName,port):
    import os
    localdir = os.getcwd()
    fPath = os.path.join(localdir, filename)

    if not os.path.exists(fPath):
        print 'Failed! File' , fPath, 'is not exists!!'
        return
    fin = open(fPath,'r')
    fout = open(outputName,'w')
    flag = False
    fout.writelines('startT,endT,startT_sec,endT_sec,duration,interval,interface,reason,route\n')
    startT,startT_sec,endT,endT_sec,interface,reason,duration,interval = \
    None, None, None, None, None, None, None, None
    lastCheck = 0.0
    for line in fin:

        if not 'System' in line: continue
        if not port in line: continue
        line = line.strip()
        #print line
        timeLine = line[:15]
        timeLine = '2016 ' + timeLine
        # start from down event
        if 'state down' in line:
            flag = True
            startT = timeLine
            startT_sec = timeModule.getMkTime(startT)
            if lastCheck == 0.0:
                interval = -1
            else:
                interval = startT_sec - lastCheck
            reason = line.split(' - ')[-1]
            interface = line.split('Interface ethernet ')[-1].split(',')[0]

        # then up event, (down - up is a flapping)    
        elif 'state up' in line and flag == True:
            flag = False
            endT = timeLine
            endT_sec = timeModule.getMkTime(timeLine)
            duration = endT_sec - startT_sec
            lastCheck = endT_sec
            wline = '{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(startT,endT, \
            startT_sec,endT_sec,duration,interval,interface,reason,outputName.split('.csv')[0])
            fout.writelines(wline)
        else: continue
    fin.close()
    fout.close()


logList = [
'NorthRoute_AMS_CHI_AmsMLXe4.log' ,
'NorthRoute_CHI_AMS_ChiMLXe4.log' ,
'NorthRoute_CHI_TPE_ChiMLXe4.log' ,
'NorthRoute_TPE_CHI_TpeMLXe8.log' ,
'SouthRoute_AMS_CHI_AmsMLXe4.log' ,
'SouthRoute_CHI_AMS_ChiMLXe4.log' ,
'SouthRoute_CHI_TPE_ChiMLXe4.log' ,
'SouthRoute_TPE_CHI_TpeMLXe8.log'
]
#for logName in logList:
#    getCSV(logName)
nDay = -1 
getCSV('CHIflapping_{0}_log'.format(timeModule.getNday(nDay)),'SouthRoute_CHI_TPE_ChiMLXe4.csv','1/11,')
getCSV('TPEflapping_{0}_log'.format(timeModule.getNday(nDay)),'SouthRoute_TPE_CHI_TpeMLXe8.csv','2/2,')
getCSV('CHIflapping_{0}_log'.format(timeModule.getNday(nDay)),'NorthRoute_CHI_TPE_ChiMLXe4.csv','1/1,')
getCSV('TPEflapping_{0}_log'.format(timeModule.getNday(nDay)),'NorthRoute_TPE_CHI_TpeMLXe8.csv','1/2,')
