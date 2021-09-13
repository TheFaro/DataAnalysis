import pandas as pd
import json
import math
import numpy
import matplotlib.pyplot as plt

df = pd.read_excel('~/Documents/Excel/test.xlsx','Data')
print(df)

df = df.dropna()
df = df.set_index('Date/Symbol')

fil = open('UI/practice/pands.txt','w')
df.to_string(fil)
fil.close()

df.plot()
plt.show()

