import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://dsk181.grid.sinica.edu.tw/LinkUsage/.bkp/asgc2nchc20160412.html'
res = requests.get(url)
msg = res.text.split('\n')
msg_ = ' '.join(msg)
#print msg_
#m = re.findall('options.series\[0\].data \= \[.*\];',msg_)
m = re.findall('(\[.*],)',(res.text))

def getFirstTime(msg):
    import re
    m = re.search('(\(.*\))',msg)
    mm = m.group(1)
    return '-'.join( mm.strip('(').strip(')').split(','))

def getAbsTime(tStr):    
    import time
    return time.mktime(time.strptime(tStr, "%Y-%m-%d-%H-%M-%S"))

print type(m)
print len(m)
#list [ [time] ,  [abstime] , [MBin] [MBout]]
mydata = [ [] , [] , [] , [] ]
firstTime = ''
for item in m:
    if not u'data' in item: continue
    firstTime = getFirstTime(item)
    break
    print '++++++++++++++++++++'
    print item
    print item.split('')
    print type(item)
    print '--------------------'

print firstTime
