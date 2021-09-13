import weo

#for(year, release) in weo.all_releases():
#    weo.download(year, release, filename="weo.csv",directory="weo_data")

w = weo.WEO("weo_data/weo.csv")

#variable listing
w.variables()

#units
print(w.units())
print(w.units("Gross domestic product, current prices"))

#variable codes
print(w.codes)
print(w.from_code("LUR"))

#countries
print(w.countries())
print(w.countries("United"))

print(w.iso_code3('Netherlands'))

#print(w.get("General government gross debt", "Percent of GDP"))
#print(w.getc("NGDP_RPCH"))
#print(w.country("DEU", 2018))

(w.gdp_usd(2005).dropna().sort_values().tail(12).plot().barh(title="GDP by country, USD bln (2024)"))