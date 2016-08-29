def getStrTime(tstr):
    import time
    return time.strptime(tstr,'%Y %b %d %H:%M:%S')

def getMkTime(tstr):
    import time
    return time.mktime(getStrTime(tstr))

def getNday(n=0):
    import time
    tm = time.localtime(time.time()+(n*86400))
    return '{0}{1:0>2d}{2:0>2d}'.format(tm.tm_year,tm.tm_mon,tm.tm_mday)

def getYesterday():
    import time
    tm = time.localtime(time.time()-86400)
    return '{0}{1:0>2d}{2:0>2d}'.format(tm.tm_year,tm.tm_mon,tm.tm_mday)

def getToday():
    import time
    tm = time.localtime(time.time())
    return '{0}{1:0>2d}{2:0>2d}'.format(tm.tm_year,tm.tm_mon,tm.tm_mday)

def getUnixDaySecond(unixtime):
    import pandas as pd
    import datetime
    temp = datetime.datetime.fromtimestamp(unixtime)
    stt = '{0}{1:0>2d}{2:0>2d}'.format(temp.year,temp.month,temp.day)
    print stt
    return pd.to_datetime(stt).value // 10 ** 9
