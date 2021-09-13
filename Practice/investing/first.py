import investpy
import json

df = investpy.get_funds(country='united states')
outfile = open('Practice/investing/first.text','w+')
#outfile.write(json.dumps(df))
df.to_string(outfile)
outfile.close()
#print(df)