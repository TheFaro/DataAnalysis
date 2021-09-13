import requests

#find series list 
url = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"
key = "Dataflow"        #method with series information
search_term = 'CPI'   #term to find in series names
series_list = requests.get(f'{url}{key}').json()\
            ['Structure']['Dataflows']['Dataflow']

#outfile = open("imf/results3.txt", "w+")
#use dict keys to navigate through results:
for series in series_list:
    #outfile.write(f'{series}\n')

    if search_term in series['Name']['#text']:
        print(f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}")

#outfile.close()

#finding the dimensions of the series
key1 = 'DataStructure/CPI'
dimension_list = requests.get(f'{url}{key1}').json()\
                ['Structure']['KeyFamilies']['KeyFamily']\
                ['Components']['Dimension']

for n, dimension in enumerate(dimension_list):
    print(f'Dimension {n+1} {dimension["@codelist"]}')


#find codes for each dimension
key2 = f"CodeList/{dimension_list[1]['@codelist']}"
code_list = requests.get(f'{url}{key2}').json()\
            ['Structure']['CodeLists']['CodeList']['Code']

for code in code_list:
    print(f"{code['Description']['#text']} : {code['@value']}")