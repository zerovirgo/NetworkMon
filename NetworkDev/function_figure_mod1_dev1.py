import matplotlib
matplotlib.use('Agg')
import pylab as plt
import pandas as pd
import numpy as np
from pandas.tools.plotting import lag_plot

def drawFlowBasic(fName):
    df = pd.read_csv(fName,index_col='startT',parse_dates=True)
    #print df.head()
    # Net flow statistics
    print df.describe()
    netinMean =  format(df.describe()['netinput']['mean'], '.1f')
    netoutMean = format( df.describe()['netoutput']['mean'], '.1f')
    netinStd =  format(df.describe()['netinput']['std'] , '.1f')
    netoutStd =  format(df.describe()['netoutput']['std'] , '.1f')
    outname = fName.split('od1_')[-1].split('.')[0]+'_netflowhist.png'
    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.15,0.25,0.8,0.65])
    bins = np.linspace(0, 800, 160)
    ax.hist(df['netinput'],bins, color='g',alpha=0.5,label='Input (MB/sec)')
    ax.hist(df['netoutput'],bins, color='b',alpha=0.5,label='Output (MB/sec)')
    ax.set_title('_'.join(fName.split('od1_')[-1].split('_')[:3])+\
    ' avg = {0}+/-{1}(in) {2}+/-{3}(out) (MB/sec)'.format(netinMean , netinStd , netoutMean , netoutStd))
    ax.set_xlabel('Network flow (MB/sec)')
    ax.set_ylabel('number of events')
    ax.legend(loc='upper right')
    plt.savefig(outname)
    plt.clf()
    
    # Net flow distribution
    outname = fName.split('od1_')[-1].split('.')[0]+'_netflowdate.png'
    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.15,0.25,0.8,0.65])
    ax= df['netinput'].plot(kind='line',color='g',alpha=0.5,label='Input (MB/sec)')
    df['netoutput'].plot(kind='line',ax = ax ,color='b',alpha=0.5,label='Output (MB/sec)')
    ax.set_title('_'.join(fName.split('od1_')[-1].split('_')[:3]))
    ax.set_xlabel('Date')
    ax.set_ylabel('Network flow (MB/sec)')
    ax.legend(loc='upper right')
    plt.savefig(outname)
    plt.clf()

    total = len(df)
    outname = fName.split('od1_')[-1].split('.')[0]+'_netlagIn.png'
    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.15,0.25,0.8,0.65])
    ax= lag_plot(df['netinput'], color='g',alpha=0.5)
    #df['netoutput'].plot(kind='line',ax = ax ,color='b',alpha=0.5,label='Output (MB/sec)')
    ax.set_title('_'.join(fName.split('od1_')[-1].split('_')[:3])+ ' input\nTotal {0} points'.format(total))
    ax.legend(loc='upper right')
    ax.set_xlabel('Network input (t) (MB/sec)')
    ax.set_ylabel('Network input (t+1) (MB/sec)')
    plt.savefig(outname)
    plt.clf()

    outname = fName.split('od1_')[-1].split('.')[0]+'_netlagOut.png'
    plt.figure(1, figsize=(12,9))
    ax = plt.axes([0.15,0.25,0.8,0.65])
    ax= lag_plot(df['netoutput'], color='b',alpha=0.5)
    #df['netoutput'].plot(kind='line',ax = ax ,color='b',alpha=0.5,label='Output (MB/sec)')
    ax.set_title('_'.join(fName.split('od1_')[-1].split('_')[:3])+ ' output\nTotal {0} points'.format(total))
    ax.legend(loc='upper right')
    ax.set_xlabel('Network output (t) (MB/sec)')
    ax.set_ylabel('Network output (t+1) (MB/sec)')
    plt.savefig(outname)
    plt.clf()

namelist = [
'mod1_NorthRoute_CHI_TPE_ChiMLXe4.csv' ,
'mod1_NorthRoute_TPE_CHI_TpeMLXe8.csv' ,
'mod1_SouthRoute_CHI_TPE_ChiMLXe4.csv' ,
'mod1_SouthRoute_TPE_CHI_TpeMLXe4.csv'
]

for name in namelist:
    drawFlowBasic(name)
