import pandas as pd

songs66 = pd.Series([3, None, 11, 9],index=['George','Ringo','John','Paul'],name='Counts')
songs69 = pd.Series([18, 22, 7, 5],index=['John','Paul','George','Ringo'],name='Counts')

for value in songs66:
    print value

for idx, value in songs66.iteritems():
    print idx, value

for idx in songs66.keys():
    print idx

songs66 + 2

print songs66

print songs66 + songs69

print songs66.fillna(0) + songs69.fillna(0)
print songs66.John

print songs66.reset_index()
print songs66.reset_index(drop=True)

print songs66.describe()