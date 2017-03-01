import pandas as pd

#ser = pd.date_range('3/21/2016' ,periods = 180, freq='D')
ser = pd.date_range('1/1/2016' ,periods = 193, freq='D')
#for tt in ser:
#    print ''.join(str(tt).split(' ')[0].split('-'))

print ser[0], ser[-1]
