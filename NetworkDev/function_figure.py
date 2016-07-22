import pandas as pd
import numpy as np
import pylab as plt
import function_df

def drawDownTimeVSInterval(filename):
    title = filename.split('.')[0]+' flapping duration v.s. interval'
    outname = filename.split('.')[0]+'fDuration_vs_fInterval'
    df = function_df.getDF_netlog(filename)
    print df.head()

    
    ax = df.plot(kind = 'scatter',x= 'duration', y = 'interval',xlim=(-10,1000),ylim=(-10,1000),figsize=(12,9))
    plt.title(title)
    plt.xlabel('Flapping duration (sec)')
    plt.ylabel('Interval between flappings (sec)')
    ax2 = df.plot(kind = 'scatter',x= 'duration', y = 'interval')
    plt.title(title)
    plt.xlabel('Flapping duration (sec)')
    plt.ylabel('Interval between flappings (sec)')
    
    ax3= df['duration'].plot(kind = 'line',ylim=(-1,44100))
    plt.xlabel('')
    print df.describe()
    title = filename.split('.')[0] + ' %d flappings\n'%(df.describe()['duration']['count'])
    title += 'From {0} to {1}'.format(df.index[0],df.index[-1])
    plt.title(title)
    

    #buffer0.index = buffer0.index.apply(lambda x : '{0}-{1}-{2}'.format(x[0],x[1],x[2]))
    #print buffer0.head()
    #plt.xlim = (-1df.plot(kind = 'scatter',x= 'duration', y = 'interval',1000)
    #plt.ylim = (-1,1000)
    #plt.savefig('test.png',format='png')


#drawDownTime('SouthRoute_CHI_TPE_TpeMLXe4.csv')
myname = 'SouthRoute_CHI_TPE_ChiMLXe4.csv'
drawDownTimeVSInterval(myname)