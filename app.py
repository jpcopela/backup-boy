import tkinter as tk
from tkinter import ttk
from src.tk_filebrowser import TKFileBrowser

#a very basic window that we will embed the file browser in
class MainWindow(tk.Tk):
    def __init__(self, width : int, height : int):
        super().__init__()
        self.title("Backup Boy")
        self.geometry(f"{width}x{height}")

        #configure the style of the treeview widget with a font that will work on raspberry pi
        self.call('source', 'resources/styles/forest-dark.tcl')
        style = ttk.Style()
        style.theme_use('forest-dark')
        style.configure("Treeview", font=(14), rowheight=32)

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
    #app.attributes("-fullscreen", True)

    app.mainloop()