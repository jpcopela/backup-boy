import tkinter as tk

#This will be the main window for the application and will run on boot
#For testing, I want to first create a basic fullscren window with a button to exit

#Create the window
window = tk.Tk()

#Set the window to fullscreen
window.attributes('-fullscreen', True)

#Create a button to exit the window
button = tk.Button(window, text = "Exit", command = window.destroy)
button.pack()

#Run the window
window.mainloop()