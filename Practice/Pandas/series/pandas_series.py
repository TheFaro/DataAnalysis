import pandas as pd
import numpy as np
songs = pd.Series([145,142,38,13],name='counts')

print songs

print songs.index

songs2 = pd.Series([145,142,38,13],name='counts',index=['Paul','John','George','Ringo'])

print songs2

nan_ser = pd.Series([2, None], index=['Ono', 'Clapton'])

print nan_ser

print nan_ser.count()

numpy_ser = np.array([145,142,38,13])
print(numpy_ser[1])

print songs2.mean()
print numpy_ser.mean()

mask = songs2 > songs2.median()
print mask

print songs2[mask]