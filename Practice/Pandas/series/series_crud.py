import pandas as pd

george_dupe = pd.Series([10,7,1,22],index=['1968','1969','1970','1970'],name='George Songs')

'''Reading or Selection'''

for item in george_dupe:
    print item

for item in george_dupe.iteritems():
    print item

'''Updating'''
george_dupe['1969'] = 6
george_dupe['1973'] = 11
george_dupe.iloc[3] = 22

print george_dupe

'''Deletion'''

del george_dupe['1969']

print george_dupe