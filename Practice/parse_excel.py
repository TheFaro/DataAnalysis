import xlrd
import pandas as pd

book = xlrd.open_workbook('~/Documents/Excel/test.xlsx')

#for sheet in book.sheets():
#    print sheet.name

print(book.user_name)
print(book.sheet_loaded(0))

print(book.nsheets)


sheet = book.sheet_by_name('Data')
#print(dir(sheet))
print('Rows:',sheet.nrows)
print('Columns:',sheet.ncols)

emptyCell = 0       # 0
textCell = 0        # 1
numberCell = 0      # 2
dateCell = 0        # 3
boolCell = 0        # 4
errCell = 0         # 5
blankCell = 0       # 6


#go through every cell and record what type of cell it is
for i in range(0,sheet.nrows):
    for j in range(0,sheet.ncols):
        #print 'Row:',i,'Col:',j,sheet.cell(i,j).value
        cellObj = sheet.cell(i,j)
        
        if cellObj.ctype == 0:
            emptyCell = emptyCell +  1
        elif cellObj.ctype == 1:
            textCell = textCell + 1
        elif cellObj.ctype == 2:
            numberCell = numberCell + 1
        elif cellObj.ctype == 3:
            dateCell = dateCell + 1
        elif cellObj.ctype == 4:
            boolCell = boolCell + 1
        elif cellObj.ctype == 5:
            errCell = errCell + 1
        elif cellObj.ctype == 6:
            blankCell = blankCell + 1

print('Empty cell No. :', emptyCell)
print('Text cell No. :', textCell)
print('Number cell No. :', numberCell)
print('Date cell No. :', dateCell)
print('Boolean cell No. :', boolCell)
print('Error cell No. :', errCell)
print('Black cell No. :', blankCell)

book.datemode = 1

for date in sheet.col(0):
    #print(date)
    #print(date.value)

    #if(date.ctype == 3):
    #    this_date = xlrd.xldate.xldate_as_datetime(date.value, book.datemode)
    #    print 'Date object',this_date.year,'-',this_date.month,'-',this_date.day

    if(date.ctype == 3):
        #if(date.value == 'Date/Symbol'):
        print(f'Date: {date.value}\n')

counter = 0

#for i in xrange(sheet.nrows):
#    if counter < 50:
#        row = sheet.row_values(i)
        #print i , row
    
#    counter += 1

'''df = pd.read_excel('~/Documents/Excel/test.xlsx')

outfile = open('dataframe/list.txt','w+')
outfile.write(df.to_string())
outfile.close()
print(df)

for row in df.itertuples():
    print(row[5])'''

print(sheet.col_label_ranges)