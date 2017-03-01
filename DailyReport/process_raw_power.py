import pandas as pd
import numpy as np
import time
import datetime
import subprocess
import timeModule

def toDateTime(seconds):
    import datatime


def raw2digi(filename,port,outputname):
    cols = [ 'tms' , 'port' , 'temp' , 'Tx' ,
        'Rx' , 'bias' ]
    df = pd.read_table(filename,sep=':',header=None)
    df.columns = cols
    dateindex = lambda x : time.gmtime(x)
    df['abstime'] = df['tms'] + 28800
    df['date'] = df['abstime'].apply(lambda x : pd.to_datetime(time.ctime(x)))
    #df['InOct'] = df['InOct'].astype(np.int64)
    fout = open('data_'+ outputname+'.csv', 'w')
    fout.writelines('date,abstime,port,temp,Tx,Rx,bias\n')
    # Define previous variables [time,input,output]
    df = df.query('port=={0}'.format(port))
    dates = []
    #print df.tail()
    for index, row in df.iterrows():
        #print pd.to_datetime(time.gmtime(row['tms']))
        #print row['Tx'], np.isnan(row['Tx'])
        if np.isnan(row['Tx']):
            continue

        #consider time difference
        #print row['tms'], type(row['tms']), row['InOct'], type(row['InOct']), np.isnan(row['InOct'])
        seconds = row['tms'] #+28800
        mt = time.localtime(seconds)
        mt = time.asctime(time.localtime(seconds)) + ' -0800'
        #dates.append(pd.to_datetime(mt))
        #print pd.to_datetime(mt)
        #print pd.to_datetime(mt), type(pd.to_datetime(mt))
        #print type(row['InOct']), row['InOct']


        #print '---------------------'
        #print datetime.fromtimestamp(time.mktime(time.gmtime(row['tms'])))
        lines = '{0},{1},{2},{3},{4},{5},{6}\n'.format(pd.to_datetime(mt),seconds+28800,row['port'],
                row['temp'],row['Tx'],row['Rx'],row['bias'])
        fout.writelines(lines)
            
    fout.close()



fname = 'TWBR2_Optical_20160809'
files = ['TWBR2_Optical_today' , 'CHIBR0_Optical_today']
copies = ['TWBR2_Optical_{0}'.format(timeModule.getToday()) , 'CHIBR0_Optical_{0}'.format(timeModule.getToday())]

start = datetime.datetime.now()
i = 0
nDay = -1
files = [
'TWBR2_Optical_{0}'.format(timeModule.getNday(nDay)),
'TWBR2_Optical_{0}'.format(timeModule.getNday(nDay)),
'CHIBR0_Optical_{0}'.format(timeModule.getNday(nDay)),
'CHIBR0_Optical_{0}'.format(timeModule.getNday(nDay))
        ]
raw2digi(files[0],66,'South_TWBR2_Optical')
raw2digi(files[1],2,'North_TWBR2_Optical')
raw2digi(files[2],11,'South_CHIBR0_Optical')
raw2digi(files[3],1,'North_CHIBR0_Optical')
#    cmd = 'cp {0} {1}'.format(item,copies[i])
#    subprocess.Popen(cmd,shell=True)
#    i += 1

end = datetime.datetime.now()
c = end - start
print 'time to run = ', c.seconds

