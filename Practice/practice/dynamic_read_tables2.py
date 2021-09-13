import xlrd

book = xlrd.open_workbook('~/Documents/Excel/test.xlsx')

sheet = book.sheet_by_name('Analysis')

#stores starts of tables
start_cells = []

#types of cells
empty_cell = 0
text_cell = 1
number_cell = 2
date_cell = 3
bool_cell = 4
error_cell = 5
blank_cell = 6

for row in range(sheet.nrows):
    for col in range(sheet.ncols):
        cell = sheet.cell(row, col)

        if cell.ctype != empty_cell:
            #check above and on the left
            try:
                above = sheet.cell(row-1,col)
                left  = sheet.cell(row,col-1)
                above_left = sheet.cell(row-1,col-1)
                
                bottom = sheet.cell(row+1,col)
                right = sheet.cell(row,col+1)
                bottom_right = sheet.cell(row+1,col+1)

                if above.ctype == empty_cell and left.ctype == empty_cell and above_left.ctype == empty_cell and bottom.ctype != empty_cell and right.ctype != empty_cell and bottom_right.ctype != empty_cell:
                    print(f'({row},{col})')
            except IndexError:
                #do something
                print(f'Exception: ({row},{col})')

