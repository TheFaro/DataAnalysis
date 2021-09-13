import pandas as pd
import itertools as it
import xlrd as xrd

'''
with('~/Documents/Excel/test.xlsx') as fp:
    skip = next(it.filter(
        lambda x: x[1].startswith('Date/Symbol'),
        enumerate(fp)
    ))[0]
'''

book = xrd.open_workbook('~/Documents/Excel/test.xlsx')

df = pd.read_excel('~/Documents/Excel/test.xlsx','Normalize',index_col=None,dtype={'Index':int,'Value':float},header=None).fillna(0.0)

print 'Column Number :', len(df.columns)
print 'Row Number: ', len(df)

for i in range(len(df)):
    for j in range(len(df.columns)):
        #print 'Row:',i,' && Column: ',j
        if df.iloc[i][j] == 'Date/Symbol':
            print 'Row:',i,' && Column: ',j


#data = df.str.find('Date/Symbol', 0)

headers = df.loc[16].to_dict()


#for i in range(len(df.nrows)):

#for key, value in df.iteritems():
#    print key, value

#for i,j in df.iterrows():
#    print i,j
#    print ' '

#for value in df.iterrows():
#    print value
    #if value == "Date/Symbol":
    #    print 'Found :', key
    #print key, value
    #print ' '

'''
index = 1
for i in df.itertuples():
    if i[index-1] == 'Date/Symbol' :
        print i[index]
    #print i[2]
    #print ''
    index = index + 1

    Definition of a function that uses pandas to read data from the excel document:
    -   it saves the row and column index values to use as a starting point for the table data, the first value on the top most left corner is the Date/Symbol text value.
    -   the function will then store the column names in a dictionary data structure where upon clicking the column name, the column index as the key will be retrieved.
    -   based on the column index, the data values beneath the column title will be read using the pandas module and be plotted using the seaborn module


def handleData(df=None):
    if(df == None):
        print 'There is no data to be worked with.'

    rowIndex = None
    columnIndex = None
    startText = 'Date/Symbol'

    #find the row and column index in the data frame
    #for row in df.iloc:
'''

'''
def parse_excel_sheet(file,sheet_name=0,threshold=5):
    ~   parses multiple tables from an excel sheet into multiple dataframe objects  ~
    x1 = pd.ExcelFile(file)
    entire_sheet = x1.parse(sheet_name=sheet_name)

    n_values = (entire_sheet.isnull()).sum(axis=1)
    n_values_deltas = n_values[1:] - n_values[:-1].values

    table_beginnings = n_values_deltas > threshold
    table_beginnings = table_beginnings[table_beginnings].index
    table_endings = n_values_deltas < -threshold
    table_endings = table_endings[table_endings].index

    if len(table_beginnings) < len(table_endings) or len(table_beginnings) > len(table_endings)+1:
        raise BaseException('Could not detect equal number of begginings and ends')

    md_beginnings = []
    for start in table_beginnings:
        md_start = n_values.iloc[:start][n_values==0].index[-1] + 1
        md_beginnings.append(md_start)

    dfs = []
    df_mds = []

    for ind in range(len(table_beginnings)):
        start = table_beginnings[ind] + 1
        if ind < len(table_endings):
            stop = table_endings[ind]
        else:
            stop = entire_sheet.shape[0]
        
        df = x1.parse(sheet_name=sheet_name, skiprows=start, nrows=stop-start)
        dfs.append(df)

        md = x1.parse(sheet_name=sheet_name,skiprows=md_beginnings[ind], nrows=start-md_beginnings[ind]-1).dropna(axis=1)
        df_mds.append(md)

    print dfs


parse_excel_sheet('~/Documents/Excel/test.xlsx','Data')'''