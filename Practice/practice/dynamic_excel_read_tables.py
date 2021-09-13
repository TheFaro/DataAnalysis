import xlrd
import pandas as pd

book = xlrd.open_workbook('~/Documents/Excel/test.xlsx')

print(book.user_name)
print(f'Number of sheets {book.nsheets}')

print('\n####################################\nFirst Sheet')
sheet = book.sheet_by_name('Data')

print(f"Number of rows that might have data: {sheet.nrows}")
print(f"Number of columns that might have data: {sheet.ncols}")

'''def readSheet(sheet):

    #local variables
    start_cell = None
    start_row = None
    start_col = None
    end_row = None
    end_column = None
    df_list = []

    #types of cells
    empty_cell = 0
    text_cell = 1
    number_cell = 2
    date_cell = 3
    bool_cell = 4
    error_cell = 5
    blank_cell = 6

    start_cells = []
    bottom_cells = []

    #read each row iterating the columns
    for col in range(sheet.ncols):
        row_list = []
        for row in range(sheet.nrows):

            cell = sheet.cell(row,col)

            try:
                if cell.ctype != empty_cell:
                    top = sheet.cell(row-1, col)
                    left = sheet.cell(row, col-1)
                    top_left = sheet.cell(row-1,col-1)

                    #print(f'Left({row},{col-1}): {left}')
                    if (top.ctype == empty_cell or top.ctype == blank_cell) and (left.ctype == empty_cell or left.ctype == blank_cell) and (top_left.ctype == empty_cell or top_left.ctype == blank_cell):
                        #end_row = findTableRowDimensions(sheet,row,col)
                        print(f'Start cell ({row,col}): {cell}')
                        start_cells.append((row,col))
                    bottom = sheet.cell(row+1,col)
                    right = sheet.cell(row,col+1)

                    if (bottom.ctype == empty_cell or bottom.ctype == error_cell) and (right.ctype != empty_cell or right != error_cell):
                        print(f'Last cell({row},{col}){sheet.cell(row,col)}')
                        
                    right = sheet.cell(row,col+1)
                    bottom = sheet.cell(row+1, col)
                    bottom_right = sheet.cell(row+1,col+1)
                    #find the last cell in the last column
                    
                    if (right.ctype == empty_cell or right.ctype == error_cell) and (bottom.ctype == empty_cell or bottom.ctype == error_cell) and (bottom_right.ctype == empty_cell or bottom_right.ctype == error_cell):
                        print(f'Last cell({row},{col}){sheet.cell(row,col)}')

                    if bottom.ctype == empty_cell or bottom.ctype == error_cell and right.ctype == empty_cell or right.ctype == error_cell:
                        print(f'Bottom row cell ({row},{col}): {sheet.cell(row,col)}')
                    

                    next_cell = sheet.cell(row+1,col)
                    if next_cell == empty_cell:
                        continue
            except IndexError:
                #print(f"Out of bounds: ({row},{col})")
                bottom_cells.append((row,col))
        #print(f'End row:{end_row}')
        #print('\n')        
        print(start_cells)
        print('\n')
        print(bottom_cells)'''

#def readTable(sheet,srow,scol,erow,ecol): 


def findTableRowDimensions(sheet,srow, scol):

    erow = None

    print(f'Start row:{srow}')
    try:
        for row in range(srow,sheet.nrows):
            erow = row
            this_cell = sheet.cell(row,scol)
            print(this_cell)
            next_cell = sheet.cell(row+1,scol)

            if next_cell.ctype == 0 or next_cell.ctype == 6:    #empty cell
                return erow
    except IndexError:
        #print('out of bounds')
        return erow

def readRows(sheet):
    #list to store row values
    row_values = []

    #types of cells
    empty_cell = 0
    text_cell = 1
    number_cell = 2
    date_cell = 3
    bool_cell = 4
    error_cell = 5
    blank_cell = 6

    start_found = False
    end_found = False

    start_row = None
    start_col = None

    end_row = None
    end_col = None
    
    skip_list = []

    for i in range(sheet.nrows):
        for j in range(sheet.ncols):
            cell = sheet.cell(i,j)
            
            if cell.ctype != empty_cell:
                if start_found == False:
                    start_row = i
                    start_col = j
                    start_found = True
                
                if end_found == False :   
                    try:
                        #check next column if empty and mark as the end
                        next_col = sheet.cell(i,j+1)
                        if next_col.ctype == empty_cell:
                            end_col = j
                    except IndexError:
                        end_col = j

                    try:
                        next_row = sheet.cell(i+1,j)
                        if next_row.ctype == empty_cell:
                            end_row = i
                    except IndexError:
                        end_row = i

                    if end_row != None and end_col != None:
                        end_found = True

    print(f'Start cell: {start_row}, {start_col}')
    print(f'End cell : {end_row}, {end_col}')

readRows(sheet)
