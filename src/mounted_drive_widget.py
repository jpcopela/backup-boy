import tkinter as tk
from tkinter import ttk

import subprocess
import shutil

class MountedStorageWidget(tk.Frame):
    def __init__(self, master, button_width : int, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.font = master.drive_button_font

        self.button_width = button_width

        self.small_storage_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/small_storage.png").zoom(2)
        self.medium_storage_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/medium_storage.png").zoom(2)
        self.large_storage_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/large_storage.png").zoom(2)
        self.no_storage_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/no_storage.png").zoom(2)
        
        self._discover_storage_devices()
        self._init_ui()

    def _discover_storage_devices(self):
        #get mounted mass storage devices
        discover_devices = subprocess.run(["bash", "/home/jackson/backup-boy/bash_scripts/connect_storage.sh"], capture_output=True)
        self.storage_paths = discover_devices.stdout.strip().decode("utf-8")

        #separate the paths into a list
        self.storage_paths = self.storage_paths.split("\n")

        #get the storage size of each device
        self.storage_sizes = []

        if (not self.storage_paths == ['']):
            #extract the storage names from the paths
            self.storage_names = [path.split("/")[-1] for path in self.storage_paths]            
            
            for path in self.storage_paths:
                #get the storage size of the device
                size = shutil.disk_usage(path).total
                #convert the size from bytes to gigabytes
                size = round(size / 1024 / 1024 / 1024, 2)
                self.storage_sizes.append(size)

            #default select the largest storage device
            self.selected_drive_index = self.storage_sizes.index(max(self.storage_sizes))
            self.selected_drive_path = self.storage_paths[self.selected_drive_index]
        
        else:
            self.storage_names = []
            self.selected_drive_index = None
            self.selected_drive_path = None

    def _init_ui(self):
        #show a border around the widget
        self.configure(borderwidth=1, relief=tk.FLAT)

        self.buttons = []

        for i in range(3):
            button = tk.Button(self, compound=tk.TOP)
            button.configure(font=self.font, width=self.button_width, wraplength=round(self.button_width * 1.5), relief=tk.FLAT)

            if i < len(self.storage_names):
                name = self.storage_names[i]
                size = self.storage_sizes[i]

                button.configure(text=f'Mass storage:\n{name}\n{size} GB')

                #make a button to contain the storage icon and the name of the storage device
                if size < 32:
                    button.configure(image=self.small_storage_icon)

                elif size < 128:
                    button.configure(image=self.medium_storage_icon)
                else:
                    button.configure(image=self.large_storage_icon)

            else:
                #make a blank button to fill the space
                button.configure(text=f"Mass storage {i + 1}:\nNot detected", image=self.no_storage_icon, state=tk.DISABLED)
                
            #bind the button to the _on_drive_selected method
            button.bind("<Button-1>", lambda event, button=button: self._on_drive_selected(button))
            button.grid(row=i, column=0, sticky=tk.NSEW)

            self.buttons.append(button)

            #highlight the button corresponding to the selected drive
            if (i == self.selected_drive_index):
                button.configure(bg="#217346")
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)

    def _on_drive_selected(self, button):
        #if its not disabled, then it is a valid drive
        if (not button["state"] == tk.DISABLED):
            #deselect the previously selected drive
            self.buttons[self.selected_drive_index].configure(bg="#313131")

            self.selected_drive_index = self.buttons.index(button)
            self.selected_drive_path = self.storage_paths[self.selected_drive_index]

            #get the button corresponding to the selected drive
            button.configure(bg="#217346")     