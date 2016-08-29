import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as plt
import time
import timeModule

def getDivs(counts,division):
    prevstat = False
    info = []
    binw = division[1] -division[0]
    start, end = None, None
    theMax = 0
    for i in range(len(counts)):
        if counts[i] != 0 and prevstat== False:
            start = division[i]
            prevstat = True
            end = division[i]
            if counts[i] > theMax:
                theMax = counts[i]
            continue
        elif counts[i] != 0 and prevstat==True:
            end = division[i]
            if counts[i] > theMax:
                theMax = counts[i]
            continue
        elif counts[i] == 0 and prevstat==True:
            info.append([start,end+binw,theMax])
            prevstat = False
            start,end = None,None
            theMax = 0
            continue
    return info

def getInterval(df,startLoc,endLoc):
    #print 'getInter df range, inputrange', df['abstime'][df.index[0]], df['abstime'][df.index[-1]], startLoc,endLoc
    #print 'getInter df range, inputrange', df['abstime'][df.index[0]]<=startLoc, df['abstime'][df.index[-1]]>= endLoc
    subdf = df.query('abstime > {0} and abstime < {1}'.format(startLoc,endLoc))
    subdff = df.query('abstime < {0}'.format(startLoc))
    if len(subdf) == 0:
        #return None,None, None
        if len(subdff)>0:
            return subdff.index[-1],subdff.index[-1], subdff.index[-1]
    else:
        print 'case2', subdff.index[-1],subdf.index[0], subdf.index[-1]
        return subdff.index[-1],subdf.index[0], subdf.index[-1]

def exeDataPross(csvpowerR,csvpowerT,csvflappingR,csvflappingT,route,startLevel):
    dfPRx = pd.read_csv(csvpowerR)
    dfPTx = pd.read_csv(csvpowerT)
    dfFRx = pd.read_csv(csvflappingR)
    dfFTx = pd.read_csv(csvflappingT)
    # get only past 24 hours's data
    queryTime = timeModule.getUnixDaySecond(dfPRx.abstime[dfPRx.index[-5]])
    dfPRx = dfPRx.query('abstime>= {0} and abstime<{1}'.format(queryTime,queryTime+86400))
    dfPTx = dfPTx.query('abstime>= {0} and abstime<{1}'.format(queryTime,queryTime+86400))
    statusArr = np.array([])
    # Label status of Rx
    indexP = dfPRx.index
    statusArr = np.array(['Normal' for i in range(0,len(indexP))])
    dfPRx['status'] = pd.Series(statusArr,index=dfPRx.index)
    for index, row in dfFRx.iterrows():
        iBefore, iStart,iEnd = getInterval(dfPRx,row['startT_sec'],row['endT_sec'])
        if iStart is not None:
            dfPRx.loc[iStart:iEnd,'status'] = 'During'
            dfPRx.loc[iBefore,'status'] = 'Before'

    # Label status of Tx
    indexP = dfPTx.index
    statusArr = np.array(['Normal' for i in range(0,len(indexP))])
    dfPTx['status'] = pd.Series(statusArr,index=dfPTx.index)
    for index, row in dfFTx.iterrows():
        iBefore, iStart,iEnd = getInterval(dfPTx,row['startT_sec'],row['endT_sec'])
        if iStart is not None:
            dfPTx.loc[iStart:iEnd,'status'] = 'During'
            dfPTx.loc[iBefore,'status'] = 'Before'

    f, axarr = plt.subplots(2,figsize=(9,12))
    #axarr[0] = plt.axes([0.15,0.15,0.6,0.7])
    #mybin =  [startLevel+i/100.0 for i in range(101)]
    mybin = np.arange(-10,-1,0.01)
    searchbin =  np.arange(-10,-1,0.005)
    rMap ={
        'North_ChiMLXe4' : 'North_TpeMLXe8' ,
        'North_TpeMLXe8' : 'North_ChiMLXe4' ,
        'South_ChiMLXe4' : 'South_TpeMLXe8' ,
        'South_TpeMLXe8' : 'South_ChiMLXe4' 
            }
    print 'Range of {0} from {1} to {2}'.format(route,mybin[0],mybin[-1])
    axarr[0].hist(dfPRx.query('status=="Normal"')['Rx'],bins=mybin,color='r',label='Rx of {0}'.format(route),edgecolor = "none")
    axarr[0].hist(dfPTx.query('status=="Normal"')['Tx'],bins=mybin,color='b',label='Tx from {0}'.format(rMap[route]),edgecolor = "none")
    axarr[0].legend(loc='upper center',ncol = 2)
    axarr[0].set_title('Rx({0}) and Tx({1})\nNormal'.format(route,rMap[route]))
    axarr[0].set_xlabel('Power level (dBm)')
    axarr[0].set_ylabel('counts')
    #plt.legend(shadow=True, fancybox=True)
    # Add messages of groups Rx and Tx
    msg = u'Rx:\n'
    maxY = 0
    myRef = 0 #to adjust plot start point
    counts, division = np.histogram( dfPRx.query('status=="Normal"')['Rx'] , bins = searchbin )
    for itv in getDivs(counts,division):
        ser = dfPRx.query('status=="Normal" and Rx > {0} and Rx <={1}'.format(itv[0],itv[1]))['Rx']
        #if ser.count() <= 3: continue
        theY = itv[2]
        if theY > maxY:
            maxY = theY
        theMean = ser.mean()
        theStd = ser.std()
        if np.isnan(ser.std()):
            print 'There is a nan!!:' ,ser
            theStd = 0.0
        msg += u'[{0:0.3f} to {1:0.3f}] :{2:0.3f} $\pm$ {3:0.3f}\n'.format(itv[0],itv[1],theMean,theStd)
        myRef =  axarr[0].get_xaxis().get_data_interval()[0]
        myRef = (myRef*10)%2
    msg += u'Tx:\n'
    counts, division = np.histogram( dfPTx.query('status=="Normal"')['Tx'] , bins = searchbin )
    for itv in getDivs(counts,division):
        ser = dfPTx.query('status=="Normal" and Tx > {0} and Tx <={1}'.format(itv[0],itv[1]))['Tx']
        #if ser.count() <= 3: continue
        theY = itv[2]
        if theY > maxY:
            maxY = theY
        theMean = ser.mean()
        theStd = ser.std()
        if np.isnan(ser.std()):
            print 'There is a nan!!:' ,ser
            theStd = 0.0
        msg += u'[{0:0.3f} to {1:0.3f}] :{2:0.3f} $\pm$ {3:0.3f}\n'.format(itv[0],itv[1],theMean,theStd)
        myRef =  axarr[0].get_xaxis().get_data_interval()[0]
        myRef = (myRef*10)%2
    if len(msg) > 5:
        print 'msg = ', msg
        axarr[0].text(startLevel-(myRef*0.1),1,msg)

    #axarr[1] = dfPRx.query('status=="During"')['Rx'].plot(kind='hist',bins=mybin,color='r',label='Rx - {0}'.format(route),edgecolor = "none")
    #dfPTx.query('status=="During"')['Tx'].plot(kind='hist',bins=mybin,ax=axarr[1],color='b',label='Tx - {0}'.format(rMap[route]),edgecolor = "none",legend=True)
    axarr[1].hist(dfPRx.query('status=="During"')['Rx'],bins=mybin,color='r',label='Rx of {0}'.format(route),edgecolor = "none")
    axarr[1].hist(dfPTx.query('status=="During"')['Tx'],bins=mybin,color='b',label='Tx from {0}'.format(rMap[route]),edgecolor = "none")
    axarr[1].legend(loc='upper center',ncol = 2)
    axarr[1].set_title('During flapping')
    axarr[1].set_xlabel('Power level (dBm)')
    axarr[1].set_ylabel('counts')

    # Add messages of groups Rx and Tx
    msg2 = u'Rx:\n'
    myRef = 0 #to adjust plot start point
    counts, division = np.histogram( dfPRx.query('status=="During"')['Rx'] , bins = searchbin )
    for itv in getDivs(counts,division):
        ser = dfPRx.query('status=="During" and Rx > {0} and Rx <={1}'.format(itv[0],itv[1]))['Rx']
        #if ser.count() <= 3: continue
        theY = itv[2]
        if theY > maxY:
            maxY = theY
        theMean = ser.mean()
        theStd = ser.std()
        msg2 += u'[{0:0.3f} to {1:0.3f}] :{2:0.3f} $\pm$ {3:0.3f}\n'.format(itv[0],itv[1],theMean,theStd)
    msg2 += u'Tx:\n'
    counts, division = np.histogram( dfPTx.query('status=="During"')['Tx'] , bins = searchbin )
    for itv in getDivs(counts,division):
        ser = dfPTx.query('status=="During" and Tx > {0} and Tx <={1}'.format(itv[0],itv[1]))['Tx']
        #if ser.count() <= 3: continue
        theY = itv[2]
        if theY > maxY:
            maxY = theY
        theMean = ser.mean()
        theStd = ser.std()
        if np.isnan(ser.std()):
            theStd = 0
        msg2 += u'[{0:0.3f} to {1:0.3f}] :{2:0.3f} $\pm$ {3:0.3f}\n'.format(itv[0],itv[1],theMean,theStd)
        myRef =  axarr[1].get_xaxis().get_data_interval()[0]
        myRef = (myRef*10)%2
    if len(msg2) > 5:
        print 'During msg2 = ' , msg2
        axarr[1].text(startLevel-(myRef*0.1),0,msg2)
        #axarr[1].annotate(msg2,xy=(startLevel-(myRef*0.1),1))


    plt.savefig('PowerDistribution_{0}_{1}.png'.format(route,timeModule.getYesterday()))
    plt.clf()
    return dfPRx

def anaData(csvpower,route,startLevel):
    dfP = pd.read_csv(csvpower)
    mybin =  [startLevel+i/100.0 for i in range(101)]
    dfdist = dfP.query('Rx > -8.0 and Rx < -5.0')['Rx']
    counts, division = np.histogram( dfdist , bins = mybin )
    for itv in  getDivs(counts,division):
        qStr = 'Rx > {0} and Rx <= {1}'.format(itv[0],itv[1])
        mean = dfP.query(qStr)['Rx'].describe().mean()
        std = dfP.query(qStr)['Rx'].describe().std()
        print dfP.query(qStr)['Rx'].describe(), u'{0} $\pm$ {1}'.format(mean,std)

now = time.time()
powerdfs = ['data_North_CHIBR0_Optical.csv', 'data_North_TWBR2_Optical.csv', 'data_South_CHIBR0_Optical.csv', 'data_South_TWBR2_Optical.csv']
flappingdfs = ['NorthRoute_CHI_TPE_ChiMLXe4.csv', 'NorthRoute_TPE_CHI_TpeMLXe8.csv' , 'SouthRoute_CHI_TPE_ChiMLXe4.csv', 'SouthRoute_TPE_CHI_TpeMLXe8.csv']
routes = ['North_ChiMLXe4', 'North_TpeMLXe8', 'South_ChiMLXe4', 'South_TpeMLXe8']
mydf = exeDataPross(powerdfs[0], powerdfs[1],flappingdfs[0],flappingdfs[1],routes[0],-10.0)
mydf = exeDataPross(powerdfs[1], powerdfs[0],flappingdfs[1],flappingdfs[0],routes[1],-10.0)
mydf = exeDataPross(powerdfs[2], powerdfs[3],flappingdfs[2],flappingdfs[3],routes[2],-10.0)
mydf = exeDataPross(powerdfs[3], powerdfs[2],flappingdfs[3],flappingdfs[2],routes[3],-10.0)
print 'Spend {0} seconds'.format(time.time()-now)
