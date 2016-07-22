import function_df

fnlist = [
'NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
'SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'SouthRoute_TPE_CHI_TpeMLXe4.csv'
]
lnlist = [
    'chi2tpe_link12016.csv' , 
    'tpe2chi_link12016.csv' , 
    'chi2tpe_link22016.csv' , 
    'tpe2chi_link22016.csv'
]

for item in zip(fnlist,lnlist):
    df1 = function_df.getDF_netlog(item[0])
    df2 = function_df.getDF_netflow(item[1])
    print item[1]
    sub1 = df1.query('duration>300.0 & startT_sec > 1457571509.0')
    iX = df1.index
    queryString = 'abstime > {0} & abstime <={1}'.format(df1.startT_sec[iX[0]],df1.startT_sec[iX[-1]])
    print sub1.head()
    #print 'avg log input = ' , format(df2.query(queryString).input.mean(),'.1f') , '+/-' , format(df2.query(queryString).input.std(), '.1f')
    #print 'avg log output = ' ,format( df2.query(queryString).output.mean(),'.1f'), '+/-' , format(df2.query(queryString).output.std(), '.1f')
    print 
    #createCSVmod1(df1,df2,'mod1_'+item[0].split('.csv')[0])
