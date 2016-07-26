import pandas as pd
import numpy as np

import pylab as plt


def getDF_summary(fName):
    df = pd.read_csv(fName,index_col='startT',parse_dates=True)
    return df


fname = 'forReport_long_flapping.csv'
df = getDF_summary(fname)

print len(df)
print 
#print df.head()
print df[df['route'].str.contains('NorthRoute_CHI_TPE_ChiMLXe4')].head()
counts  = df.route.value_counts()
countsP = df.query('planned=="P"').route.value_counts()
countsNP = df.query('planned=="NP"').route.value_counts()
countsUn = df[df['reason'].str.contains('unknown')].route.value_counts()
print counts
print countsP
print countsNP
print countsUn

#ax = plt.axes([0.15,0.25,0.8,0.65])

