import xlrd
from Tkinter import *

#this file will be modified to extend Thread which allows the script to run in the background and concurrently with the main program

#global variables
sheetNames = []

#instantiate the test excel file
book = xlrd.open_workbook('~/Documents/Excel/test.xlsx')

#get the list of sheets
for sheet in book.sheets():
    sheetNames.append(sheet.name)

#instantiate a window to display the sheet names as Buttons
root = Tk()

for sheetItem in sheetNames:
    Button(root, text=sheetItem).pack()



if __name__ == '__main__': root.mainloop()