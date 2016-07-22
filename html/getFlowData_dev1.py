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
    print mmm
    return '-'.join( mmm[:3])+' '+':'.join(mmm[3:])

def getAbsTime(tStr):    
    import time
    return time.mktime(time.strptime(tStr, "%Y-%m-%d %H:%M:%S"))

url = 'http://dsk181.grid.sinica.edu.tw/LinkUsage/.bkp/asgc2nchc20160412.html'
url = 'http://dsk181.grid.sinica.edu.tw/LinkUsage/.bkp/chi2tpe_link220160322.html'
res = requests.get(url)
#os.exit()
msg = res.text.split('\n')
msg_ = ' '.join(msg)
#print msg_
#m = re.findall('options.series\[0\].data \= \[.*\];',msg_)
m = re.findall('(\[.*],)',(res.text))

print type(m)
print len(m)
#list [ [time] ,  [abstime] , [MBin] [MBout]]
mydata = [ [] , [] , [] , [] ]
firstTime = ''
firstMsg = 'hahahaefwarioj'
countFirst = 0;
for item in m:
    #if not u'data' in item: continue
    if not u'Date' in item: continue
    if firstMsg in item:
        countFirst += 1
    if firstTime == '':
        firstTime = getStrTime(item)
        firstMsg = getStrTimeNorm(item)
    if countFirst >= 3: break
    # split messages like that: [Date.UTC(2016,3,12,00,18,45), 0],
    if countFirst == 1:
        mydata[0].append(getStrTime(item))
        mydata[1].append(getAbsTime(getStrTime(item)))
        mydata[2].append(item.split('],')[0].split(',')[-1])
    if countFirst == 2:
        mydata[3].append(item.split('],')[0].split(',')[-1])
    print '++++++++++++++++++++'
    print item
    #print item.split('')
    print type(item)
    print '--------------------'

print countFirst
print firstTime
print len(mydata[0]), len(mydata[3])
print mydata[0][-1], mydata[1][-1],mydata[2][-1],mydata[3][-1]
