import pandas as pd

ser = pd.date_range('3/21/2016' ,periods = 113, freq='D')
for tt in ser:
    print ''.join(str(tt).split(' ')[0].split('-'))
