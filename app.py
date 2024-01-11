""" import tkinter as tk
from src.tk_filebrowser import TKFileBrowser

#a very basic window that we will embed the file browser in
class MainWindow(tk.Tk):
    def __init__(self, width : int, height : int):
        super().__init__()
        self.title("Main Window")
        self.geometry(f"{width}x{height}")

        self.width=width
        self.height=height

        self._init_ui()

    def _init_ui(self):
        #the first file browser will be on the left side of the window
        self.left_file_browser = TKFileBrowser("/home/jackson")
        self.left_file_browser.grid(row=1, column=1, sticky=tk.NSEW)

        #the second file browser will be on the right side of the window
        self.right_file_browser = TKFileBrowser("/home/jackson")
        self.right_file_browser.grid(row=1, column=2, sticky=tk.NSEW)

        #configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #make it exit when escape is pressed
        self.bind("<Escape>", self.exit)

    def exit(self, event):
        self.destroy()

if __name__ == "__main__":
    app = MainWindow(800, 600)
    app.attributes("-fullscreen", True)

    app.mainloop() """

from tkinter import *
from tkinter import font

root = Tk()
root.title('Font Families')
fonts=list(font.families())
fonts.sort()

def populate(frame):
    '''Put in the fonts'''
    listnumber = 1
    for item in fonts:
        label = "listlabel" + str(listnumber)
        label = Label(frame,text=item,font=(item, 16)).pack()
        listnumber += 1

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = Canvas(root, borderwidth=0, background="#ffffff")
frame = Frame(canvas, background="#ffffff")
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

populate(frame)

root.mainloop()