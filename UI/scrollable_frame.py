import tkinter as tk
from tkinter import ttk

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self,width=container.width/2,height=container.height)
        self.scrollbar = ttk.Scrollbar(container,orient='vertical',command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0),window=self.scrollable_frame,anchor='nw')
        canvas.configure(yscrollcommand=self.scrollbar.set)
        canvas.pack(side='left',fill='both',expand=True)
        self.scrollbar.pack(side='right',fill='y')
    
    def destroyMe(self):
        print(self.winfo_class)
        self.scrollbar.destroy()
        self.destroy()
