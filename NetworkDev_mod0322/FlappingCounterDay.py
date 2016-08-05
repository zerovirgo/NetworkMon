import function_df
import pandas as pd
import time 

def get_today():
    return time.ctime(time.time())

listFiles = [
'NorthRoute_AMS_CHI_AmsMLXe4.csv' ,
'NorthRoute_CHI_AMS_ChiMLXe4.csv' ,
'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
'SouthRoute_AMS_CHI_AmsMLXe4.csv' ,
'SouthRoute_CHI_AMS_ChiMLXe4.csv' ,
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe8.csv' ]

routes = [
'NorthRoute_AMS_CHI_AmsMLXe4' ,
'NorthRoute_CHI_AMS_ChiMLXe4' ,
'NorthRoute_CHI_TPE_ChiMLXe4' ,
'NorthRoute_TPE_CHI_TpeMLXe8' ,
'SouthRoute_AMS_CHI_AmsMLXe4' ,
'SouthRoute_CHI_AMS_ChiMLXe4' ,
'SouthRoute_CHI_TPE_ChiMLXe4' ,
'SouthRoute_TPE_CHI_TpeMLXe8' ]

dflist = [function_df.getDF_netlog(x) for x in listFiles ]

newdf = function_df.getDF_netlog_total( dflist ).sort_values(['startT_sec','endT_sec'])
counts = newdf['route'].value_counts()
today = pd.to_datetime(get_today())
dRange = pd.to_datetime('20160322').dayofyear - pd.to_datetime('20160715').dayofyear
dayser = pd.date_range('20160322', periods=115, freq='d')
newdf['startT'] = newdf.index

routeDFList = [ newdf.query('route=="{0}"'.format(x)) for x in routes ]
fout = open('flappingFreqPerDay.csv','w')
fout.writelines('date,{0}\n'.format(','.join(routes)))
for day in dayser:
    infos = []
    for df in routeDFList:
        infos.append(df[df.endT.apply(lambda x : pd.to_datetime(x).dayofyear) == day.dayofyear]['route'].count())
    #print day.date(),',' , ','.join(map(str,infos))
    line = '{0},{1}\n'.format(day.date(),','.join(map(str,infos)))
    fout.writelines(line)
fout.close()
