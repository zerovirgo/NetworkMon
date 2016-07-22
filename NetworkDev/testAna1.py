# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 06:41:22 2016

@author: kschen
"""

import function_df

myname = 'SouthRoute_CHI_TPE_ChiMLXe4.csv'
oldDF = function_df.getDF_netlog(myname)
newDF = function_df.dfGroupByDay(oldDF)

print newDF.head()