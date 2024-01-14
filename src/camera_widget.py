import tkinter as tk
from tkinter import ttk

import subprocess

#this widget will display any detected cameras as buttons
class CameraWidget(tk.Frame):
    def __init__(self, master, button_width : int, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.button_width = button_width
        
        self.font = master.drive_button_font

        self.camera_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/camera_icon.png").zoom(2)
        self.no_camera_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/no_camera_icon.png").zoom(2)
        
        self._discover_storage_devices()
        self._init_ui()

    def _discover_storage_devices(self):
        #get mounted mass storage devices
        discover_devices = subprocess.run(["bash", "/home/jackson/backup-boy/bash_scripts/connect_cameras.sh"], capture_output=True)
        self.device_names = discover_devices.stdout.strip().decode("utf-8")

        #separate the paths into a list
        self.device_names = self.device_names.split("\n")

        if (not self.device_names == ['']):
            #default select the first camera
            self.selected_device_index = 0
        else:
            self.device_names = []
            self.selected_device_index = None

        
        

    def _init_ui(self):
        self.buttons = []

        for i in range(3):
            button = tk.Button(self, compound=tk.TOP)
            button.configure(font=self.font, width=self.button_width, wraplength=round(self.button_width * 1.5), relief=tk.FLAT)

            if i < len(self.device_names):
                name = self.device_names[i]

                button.configure(text=f'Camera detected:\n{name}', image=self.camera_icon)

            else:
                #make a blank button to fill the space
                button.configure(text=f"Camera {i + 1}:\nNot detected", image=self.no_camera_icon, state=tk.DISABLED)
                
            #bind the button to the _on_drive_selected method
            button.bind("<Button-1>", lambda event, button=button: self._on_drive_selected(button))
            button.grid(row=i, column=0, sticky=tk.NSEW)

            self.buttons.append(button)

            #highlight the button corresponding to the selected drive
            if (i == self.selected_device_index):
                button.configure(bg="#217346")
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)

    def _on_drive_selected(self, button):
        #if its not disabled, then it is a valid drive
        if (not button["state"] == tk.DISABLED):
            #deselect the previously selected drive
            self.buttons[self.selected_device_index].configure(bg="#ffffff")

            self.selected_device_index = self.buttons.index(button)
            self.selected_device = self.device_names[self.selected_device_index]

            #get the button corresponding to the selected drive
            button.configure(bg="#217346")  