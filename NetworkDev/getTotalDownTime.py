import function_df
import time

fname= 'NorthRoute_TPE_CHI_TpeMLXe8.csv'
mydf = function_df.getDF_netlog(fname)
dwonNto =  mydf['duration'].sum()

fname= 'NorthRoute_CHI_TPE_ChiMLXe4.csv'
mydf = function_df.getDF_netlog(fname)
downNget = mydf['duration'].sum()

fname= 'SouthRoute_TPE_CHI_TpeMLXe4.csv'
mydf = function_df.getDF_netlog(fname)
dwonSto =  mydf['duration'].sum()

fname= 'SouthRoute_CHI_TPE_ChiMLXe4.csv'
mydf = function_df.getDF_netlog(fname)
downSget = mydf['duration'].sum()


print 'NorthRoute_TPE_CHI_TpeMLXe8' , dwonNto / 3600.
print 'NorthRoute_CHI_TPE_ChiMLXe4' , downNget / 3600.
print 'SouthRoute_TPE_CHI_TpeMLXe4' , dwonSto / 3600.
print 'SouthRoute_CHI_TPE_ChiMLXe4' , downSget / 3600.
