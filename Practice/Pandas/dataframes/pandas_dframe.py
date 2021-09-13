import pandas as pd

df = pd.DataFrame({
    'growth':[.5,.7,1.2],
    'Name' : ['Paul','George','Ringo']
})

print df

print df.iloc[2]

print df['Name']

print df.axes[1]