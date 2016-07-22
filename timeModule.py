def getStrTime(tstr):
    import time
    return time.strptime(tstr,'%Y %b %d %H:%M:%S')

def getMkTime(tstr):
    import time
    return time.mktime(getStrTime(tstr))

