import requests
import re
import pandas as pd
import os
from bs4 import BeautifulSoup



def getStrTimeNorm(msg):
    import re
    m = re.search('(\(.*\))',msg)
    mm = m.group(1)
    mmm = mm.strip('(').strip(')')
    return mmm

def getStrTime(msg):
    import re
    m = re.search('(\(.*\))',msg)
    mm = m.group(1)
    mmm = mm.strip('(').strip(')').split(',')
    #print mmm
    return '-'.join( mmm[:3])+' '+':'.join(mmm[3:])

def getAbsTime(tStr):    
    import time
    return time.mktime(time.strptime(tStr, "%Y-%m-%d %H:%M:%S"))

def adjustTime(inMsg):
    if u'2016,0,' in inMsg:
        return inMsg.replace(u'2016,0', u'2016,1')
    if u'2016,1,' in inMsg:
        return inMsg.replace(u'2016,1', u'2016,2')
    if u'2016,2,' in inMsg:
        return inMsg.replace(u'2016,2', u'2016,3')
    if u'2016,3,' in inMsg:
        return inMsg.replace(u'2016,3', u'2016,4')
    if u'2016,4,' in inMsg:
        return inMsg.replace(u'2016,4', u'2016,5')
    if u'2016,5,' in inMsg:
        return inMsg.replace(u'2016,5', u'2016,6')
    if u'2016,6,' in inMsg:
        return inMsg.replace(u'2016,6', u'2016,7')
    if u'2016,7,' in inMsg:
        return inMsg.replace(u'2016,7', u'2016,8')

def writeHtmlToCSV(url,name,date):
    fname = name+date+'.csv'
    res = requests.get(url)
    msg = res.text.split('\n')
    msg_ = ' '.join(msg)
    print 'url = ' ,url
    print 'len_msg = ', len(msg)
    m = re.findall('(\[.*],)',(res.text))
    #list [ [time] ,  [abstime] , [MBin] [MBout]]
    mydata = [ [] , [] , [] , [] ]
    firstTime = ''
    firstMsg = 'hahahaefwarioj'
    countFirst = 0;
    for item in m:
        #if not u'data' in item: continue
        if not u'Date' in item: continue
        if u'2016' in item:
            item = adjustTime(item)

        if firstTime == '':
            firstTime = getStrTime(item)
            firstMsg = getStrTimeNorm(item)
        if firstMsg in item:
            countFirst += 1
        if countFirst >= 3: break
        # split messages like that: [Date.UTC(2016,3,12,00,18,45), 0],
        if countFirst == 1:
            mydata[0].append(getStrTime(item))
            mydata[1].append(getAbsTime(getStrTime(item)))
            mydata[2].append(item.split('],')[0].split(',')[-1])
        if countFirst == 2:
            mydata[3].append(item.split('],')[0].split(',')[-1])

    # start to write data
    fout = open(fname,'w')
    for i in range(0,len(mydata[0])):
        wline = '{0},{1},{2},{3}\n'.format(mydata[0][i],mydata[1][i],mydata[2][i],mydata[3][i])
        fout.writelines(wline)
    fout.close()


baseurl = 'http://dsk181.grid.sinica.edu.tw/LinkUsage/.bkp/'
baseurl = 'http://linkusage.twgrid.org/report/'
names = [ 'chi2tpe_link1' , 'chi2tpe_link2', 'tpe2chi_link1' , 'tpe2chi_link2' ]

dateList = []
#ser = pd.date_range('7/10/2016' ,periods = 2, freq='D')
ser = pd.date_range('1/1/2016' ,periods = 194, freq='D')
for tt in ser:
    dateList.append( ''.join(str(tt).split(' ')[0].split('-')) )
#print ser[0], ser[-1]
for iname in names:
    for idate in dateList:
        turl = baseurl + iname + idate + '.html'
        #print turl
        writeHtmlToCSV(turl,iname,idate)
