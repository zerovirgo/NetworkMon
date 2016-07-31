import function_df

csvlist = [
'NorthRoute_AMS_CHI_AmsMLXe4.csv' ,
'NorthRoute_CHI_AMS_ChiMLXe4.csv' ,
'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
'SouthRoute_AMS_CHI_AmsMLXe4.csv' ,
'SouthRoute_CHI_AMS_ChiMLXe4.csv' ,
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe8.csv'
]

dictRoute = {
        'NorthRoute_AMS_CHI_AmsMLXe4' : 'North_CHI_AmsMLXe4',
        'NorthRoute_CHI_AMS_ChiMLXe4' : 'North_AMS_ChiMLXe4',
        'NorthRoute_CHI_TPE_ChiMLXe4' : 'North_TPE_ChiMLXe4',
        'NorthRoute_TPE_CHI_TpeMLXe8' : 'North_CHI_TpeMLXe8',
        'SouthRoute_AMS_CHI_AmsMLXe4' : 'South_CHI_AmsMLXe4',
        'SouthRoute_CHI_AMS_ChiMLXe4' : 'South_AMS_ChiMLXe4',
        'SouthRoute_CHI_TPE_ChiMLXe4' : 'South_TPE_ChiMLXe4',
        'SouthRoute_TPE_CHI_TpeMLXe8' : 'South_CHI_TpeMLXe8' }

dflist = []
for i in csvlist:
    dflist.append( function_df.getDF_netlog(i)  )

newdf = function_df.getDF_netlog_total( dflist ).sort_index()

#newdf.query('duration > 3600').duration.plot(kind='bar',logy = True)
longDur = newdf.query('duration > 3600')

fout = open('FlappingHoursLog.csv','w')
fout.writelines('Start,End,Duration,Route\n')
for index ,row in longDur.iterrows():
    print 'Start',index ,'| End',row['endT'], '| Duration:', row['duration'], '|Route:', dictRoute[row['route']] 
    line = '{0},{1},{2},{3},\n'.format(index,row['endT'],row['duration'],dictRoute[row['route']])
    fout.writelines(line)
fout.close()
