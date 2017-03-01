import pandas as pd
import os
import function_df


def flappingChecker(df1, df2):
    indexFlow = df2.index 
    iIn = 0
    iMax = len(df2.index)
    for ind1, row1 in df1.iterrows():
        if row1.duration > 600:
            #print 'From ', ind1, 'to' , row1.endT, row1.route
            checkStart = None
            checkEnd = None
            #print "++++++++++++"
            #print row1
            while df2.abstime[indexFlow[iIn]] <  row1.startT_sec:
                if iIn >= iMax:
                    print 'Eror , reach the EOF'
                    break
                iIn += 1
            if df2.abstime[indexFlow[iIn]] >=  row1.startT_sec:
                checkStart = iIn
                check = 0
                startFlow = df2.input[indexFlow[iIn]]
                while df2.abstime[indexFlow[iIn]] <  row1.endT_sec:
                    iIn += 1
                    if check <= 3 and df2.input[indexFlow[iIn]] > 1.0e-03:
                        check += 1
                        print 'Netflow at ', str(df2.date[indexFlow[iIn]]), df2.input[indexFlow[iIn]]
                    if iIn >= iMax:
                        print 'Eror , reach the EOF'
                        break
                checkEnd = iIn-1
                if check > 1:
                    print 'This log have problem at :',ind1,'|', row1.endT,'|', str(df2.date[indexFlow[checkEnd]]),row1['route']
                    print 'Problem flow = ',startFlow ,df2.input[indexFlow[checkEnd]]
                    print 'check = ', check
            #print "------------", checkStart, checkEnd
            #print 'tme diff = ',df2.abstime[indexFlow[checkEnd]] - df2.abstime[indexFlow[checkStart]]

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

flowList = [
        'chi2tpe_link12016.csv' ,
        'tpe2chi_link12016.csv' ,
        'chi2tpe_link22016.csv' ,
        'tpe2chi_link22016.csv' 
        ]

flappingChecker(function_df.getDF_netlog(csvlist[2]),function_df.getDF_netflow(flowList[0]))
#print 'step2'
#flappingChecker(function_df.getDF_netlog(csvlist[7]),function_df.getDF_netflow(flowList[3]))
