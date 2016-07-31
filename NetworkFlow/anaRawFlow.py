import pandas as pd
import pylab as plt
import numpy as np
import sys
sys.path.append("../NetworkDev")
import function_df
import time

class analyzer:
    def __init__(self, fileFlowName,fileLogName):
        self.dfNet = self.getDF(fileFlowName)
        self.dfLog = function_df.getDF_netlog(fileLogName)

    def getDF(self, filename = 'raw_SouthRoute2016.csv'):
        df = pd.read_csv(filename,header=None)
        df.columns = np.array(['date','timesec','input','output','inputflow','outputflow'])

        #print df.head()
        ser = pd.to_datetime(df.date)
        df.index = ser
        return df
    def getFlappingListFromRawFlow(self,fout):
        infos = []
        info = []
        # record last rows have net flow
        previous = None
        previousstart = None
        previousend = None
        
        threshold = 10e-5
        duration = 0
        interval = 0
        accumulate = 0
        netflow = 0
        l_dateStart     = []
        l_dateEnd       = []
        l_dateStart_sec = []
        l_dateEnd_sec   = []
        l_duration      = []
        l_interval      = []
        l_netflow       = []
        l_accumulate    = []
        checkpoint = 1466812855
        for index, row in self.dfNet.iterrows():
            if previousend is None and row['inputflow'] > threshold:
                previousstart = row
                continue
            elif row['inputflow'] <= threshold:
                previousend = row
                continue

            # start to calculate something
            # input should > threshold

            else: 
                #print type(previousstart), type(previousend), type(previous)
                if previousend is None:
                    print row['timesec']
                    print previousstart
                #break
                duration = previousend['timesec'] - previousstart['timesec']
                netflow = previousstart['inputflow']
                if previous is None:
                    interval = -1
                    accumulate = 0
                else:
                    interval = previousstart['timesec'] -previous['timesec']
                    accumulate = float(previousstart['input']) - float(previous['input'])
                    accumulate = accumulate// float(10**9)
                    if accumulate < 0:
                        accumulate = 0
                if previousstart['timesec'] < checkpoint and previousend['timesec'] > checkpoint:
                    continue
                l_dateStart.append(previousstart['date'])
                l_dateEnd.append(previousend['date'])
                l_dateStart_sec.append(previousstart['timesec'])
                l_dateEnd_sec.append(previousend['timesec'])
                l_duration.append(duration)
                l_interval.append(interval)
                l_netflow.append(netflow)
                l_accumulate.append(accumulate)
                # reset check points
                previous = previousend
                previousend = None
                previousstart = row

        df_rec = pd.DataFrame({ 'dateIndex' : l_dateStart ,
            'StartT'     : l_dateStart ,
            'EndT'       : l_dateEnd   ,
            'startT_sec' : l_dateStart_sec ,
            'endT_sec'   : l_dateEnd_sec ,
            'duration'   : l_duration ,
            'interval'   : l_interval ,
            'netflow'    : l_netflow  ,
            'accumulate' : l_accumulate    
            } )
        df_rec.to_csv(fout)

#anaRaw()
netlogPath = '../NetworkDev/SouthRoute_TPE_CHI_TpeMLXe8.csv'
netflowPath = 'raw_SouthRoute2016.csv'
#df = getdf.getDF_netlog('../NetworkDev/SouthRoute_TPE_CHI_TpeMLXe8.csv')
#print df.head()
start = time.time()
obj = analyzer(netflowPath,netlogPath)
obj.getFlappingListFromRawFlow('flappingFromNetflow.csv')
end = time.time()
print 'Total {0} seconds spent'.format(end-start)
