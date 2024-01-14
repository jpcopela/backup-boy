import tkinter as tk
from tkinter import ttk
from src.tk_filebrowser import TKFileBrowser
from src.mounted_drive_widget import MountedStorageWidget
from src.camera_widget import CameraWidget

#a very basic window that we will embed the file browser in
class MainWindow(tk.Tk):
    def __init__(self, width : int, height : int):
        super().__init__()
        self.title("Backup Boy")
        self.geometry(f"{width}x{height}")

        self.file_browser_font = ('DejaVu Sans', 24)
        self.drive_button_font = ('DejaVu Sans', 16)

        #configure the style of the treeview widget with a font that will work on raspberry pi
        self.call('source', '/home/jackson/backup-boy/resources/styles/forest-light.tcl')
        self.style = ttk.Style()
        self.style.theme_use('forest-light')

        #get the screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.width=width
        self.height=height

        self._init_ui()

    def _init_ui(self):
        #initialize a mounted_drive_widget on the right side of the window
        self.mounted_drive_widget = MountedStorageWidget(self, button_width=round(self.width / 6))
        self.mounted_drive_widget.grid(row=0, column=3, sticky=tk.NSEW, rowspan=4)

        storage_path = self.mounted_drive_widget.selected_drive_path if self.mounted_drive_widget.selected_drive_path else "/home/jackson"

        #the second file browser will be on the right side of the window
        self.right_file_browser = TKFileBrowser(self, storage_path, autoscroll=True)
        self.right_file_browser.grid(row=1, column=2, sticky=tk.NSEW)

        #initialize a camera_widget on the left side of the window
        self.camera_widget = CameraWidget(self, button_width=round(self.width / 6))
        self.camera_widget.grid(row=0, column=0, sticky=tk.NSEW, rowspan=4)

        #the first file browser will be on the left side of the window
        self.left_file_browser = TKFileBrowser(self, "/home/jackson", autoscroll=True)
        self.left_file_browser.grid(row=1, column=1, sticky=tk.NSEW)

        #create a progress bar that will appear at the top of the window
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=self.width)
        self.progress_bar.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW)

        #configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)
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

    app.mainloop()