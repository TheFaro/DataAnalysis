import pandas as pd

george = pd.Series([10,7],index=['1968','1969'],name='George Songs')

print george

print george.index

dupe = pd.Series([10,2,7],index=['1968','1968','1969'],name='George Songs')

print dupe.index.is_unique
print george.index.is_unique

george_dupe = pd.Series([10,7,1,22],index=['1968','1969','1970','1970'],name='George Songs')

print george_dupe.at['1970']
print george_dupe.loc['1970']