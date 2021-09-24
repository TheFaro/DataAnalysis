import tkinter as tk
import tkinter.filedialog as fd

import select_sheet_frame


class SelectFileFrame(tk.Frame):
    def __init__(self, master):
        # call super class Frame constructor
        tk.Frame.__init__(self, master)

        # class variable to store the file path to display on label
        self.filename = tk.StringVar()

        # to handle back pressed from SelectSheet class
        if master.mFilePath == None:
            self.filename.set('No file selected.')
        else:
            self.filename.set(master.mFilePath)

        # build widgets for this frame

        # button to open the file from the Operating system
        self.openBtn = tk.Button(
            self, text='Open File', command=lambda: self.openFilePath(master))
        self.openBtn.pack(pady=12, ipadx=60, ipady=5)

        # label to display the path to the file
        self.filepath = tk.Label(self, textvariable=self.filename)
        self.filepath.config(bg='white', fg='black')
        self.filepath.pack(pady=12, ipadx=60, ipady=5)

        # next button to continue with the process
        self.nextBtn = tk.Button(
            self, text='Next', command=lambda: master.switch_frame(select_sheet_frame.SelectSheet))
        self.nextBtn.pack(pady=50, ipadx=20, ipady=5, side=tk.RIGHT)

        # back button
        self.backBtn = tk.Button(
            self, text='Back', command=lambda: self.goBack(master))
        self.backBtn.pack(pady=20, ipadx=20, ipady=5, side=tk.RIGHT)

    def goBack(self, master):
        import menu_frame
        master.switch_frame(menu_frame.MenuFrame)

    # function to retrieve the file to be opened
    def openFilePath(self, master):
        filepath = fd.askopenfilename(filetypes=[(
            'Excel Files', '*.xlsm'), ('Excel Files', '*.xlsx'), ('All Files', '*.*')])

        if filepath is not None:

            # set the filename to display on the label
            self.filename.set(filepath)

            # set the root class file path variable
            master.setFilePath(filepath)
