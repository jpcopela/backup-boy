import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter.filedialog import asksaveasfilename

import os
import time

#Since tkinter filedialogs are derived from the OS, they cannot be embedded in a tkinter window. 
#I will therefore have to make my own tkinter-based file browser using a treeview widget.
class TKFileBrowser(tk.Frame):
    def __init__(self, master, root : str, autoscroll : bool = False):
        super().__init__(master)

        style = master.style
        style.configure("Treeview", font=master.file_browser_font, rowheight=64)
        #create lines between the items
        style.configure("Treeview", indent=0)

        #list of directories
        self.directories = []
        #list of populated directories

        self.root_name = root
        self.autoscroll = autoscroll
        self._initialize_tree()

    #initialize the treeview widget and populate the root directory
    def _initialize_tree(self):
        self.tree = ttk.Treeview(self, show="tree", selectmode="browse", height=4)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.empty_folder_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/empty_folder.png")
        self.full_folder_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/full_folder.png")
        self.photo_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/image_icon.png")
        self.video_icon = tk.PhotoImage(file="/home/jackson/backup-boy/resources/icons/video_icon.png")
    
        #self.tree.heading("#0", text=self.root_name, anchor=tk.W)
        root_node = self.tree.insert("", tk.END, text=self.root_name, open=True)

        #populate the tree with the contents of the root directory
        self._populate_tree(root_node, self.root_name)

        #populate the tree with the contents of the root directory and its children
        children = self.tree.get_children(item=root_node)

        for item_id in children:
            item_name = self.tree.item(item_id, "text")
            item_path = self.root_name + '/' + item_name

            if (item_path in self.directories):
                self._populate_tree(item_id, item_path)

        self.tree.bind("<Button-1>", self._on_click)
        #self.tree.bind("<Double-Button-1>", self._on_click)
        self.tree.bind("<Button-3>", self._on_right_click)
        self.tree.bind("<Motion>", self._on_motion)

    #populate the tree with the contents of a directory
    def _populate_tree(self, dir_id : str, full_path : str = None) -> list:
        #add the files and directories but ignore hidden ones
        contents = [file for file in self._search_directory(full_path) if not file.startswith(".")]

        #variable for storing the index of the node
        index = 0

        #add the contents to the tree
        for item in contents:
            #find out if the item already exists in the tree
            item_id = self.tree.insert(dir_id, index, text=item)
            #get the full path of the item
            full_item_path = full_path + '/' + item

            #if the item is a directory, log it and set its icon
            if os.path.isdir(full_item_path):
                self.directories.append(full_item_path)

                is_empty = len(os.listdir(full_item_path)) == 0

                if (is_empty):
                    self.tree.item(item_id, image=self.empty_folder_icon)
                else:
                    self.tree.item(item_id, image=self.full_folder_icon)

            elif item.endswith((".png", ".jpg", ".jpeg", ".ARW", ".arw", ".tif", ".tiff", ".gif", ".bmp")):
                self.tree.item(item_id, image=self.photo_icon)

            elif item.endswith((".mp4", ".mov", ".avi", ".wmv", ".flv", ".mkv", ".webm", ".gifv")):
                self.tree.item(item_id, image=self.video_icon)

            index += 1

        return contents   

    def _search_directory(self, dir : str):
        #get the contents of the directory
        contents = os.listdir(dir)
        #sort the contents
        contents.sort()

        return contents
    
    #recursively get the parent of a given item
    #if the item is the root, return it
    def _get_full_path(self, item_id : str, initial_path : str):
        parent_id = self.tree.parent(item_id)
        parent_text = self.tree.item(parent_id, "text")

        if (parent_id == ''):
            return initial_path
        else:
            path = parent_text + '/' + initial_path

            return self._get_full_path(parent_id, path)

    def _on_click(self, event):
        #get the item that was clicked
        item_id = self.tree.identify_row(event.y)

        #get the text of the item
        item_text = self.tree.item(item_id, "text")

        full_path = self._get_full_path(item_id, item_text)

        #if it is the first time the item has been clicked, populate it
        if (full_path in self.directories):

            #if it is not already open, open it
            if (not self.tree.item(item_id, "open")):
                self.tree.item(item_id, text=item_text, open=True)
            #otherwise, close it
            else:
                self.tree.item(item_id, text=item_text, open=False)

            #get the children of the item
            children = self.tree.get_children(item_id)

            for child in children:
                child_text = self.tree.item(child, "text")
                full_child_path = full_path + '/' + child_text

                #if it is a directory, populate it
                if (os.path.isdir(full_child_path)):
                    self._populate_tree(child, full_child_path)

    def _on_right_click(self, event):
        #get the item that was clicked
        item_id = event.widget.identify_row(event.y)

        #make the item selected
        self.tree.selection_set(item_id)

        #get the text of the item
        item_text = self.tree.item(item_id, "text")
        full_path = self._get_full_path(item_id, item_text)

        #open a list of options and make it so that if the user mouses away from the menu, it closes
        menu = tk.Menu(self, tearoff=0)
        menu.configure(font=self.master.file_browser_font)

        menu.add_command(label="Rename", command=lambda: self._rename(item_id, full_path))
        menu.add_command(label="Delete", command=lambda: self._delete(item_id, full_path))
        menu.add_command(label="Copy", command=lambda: self._copy(item_id, full_path))
        menu.add_command(label="Cut", command=lambda: self._cut(item_id, full_path))
        menu.add_command(label="Paste", command=lambda: self._paste(item_id, full_path))

        #if the item is a directory, add the option to set it as the backup target
        if (full_path in self.directories):
            menu.add_command(label="Back up to this folder?", command=lambda: self._change_backup_folder(item_id, full_path))
        
        #display the menu
        menu.post(event.x_root, event.y_root)
        #close it if the user has moused away
        menu.bind("<Leave>", lambda event: menu.destroy())

    def _on_motion(self, event):
        y = event.y
        height = self.tree.winfo_height()
        
        #if the mouse is in the top 10% of the window, scroll up
        if (event.y <= height * 0.2):
            self.tree.yview_scroll(-1, "units")
            time.sleep(0.05)
        #if the mouse is in the bottom 10% of the window, scroll down
        elif (event.y >= height * 0.8):
            self.tree.yview_scroll(1, "units")
            time.sleep(0.05)

    def _rename(self, item_id : str, full_path : str):
        text = self.tree.item(item_id, "text")

        #open a dialog for the user to enter the new name with the current name as the default
        new_name, new_path = RenameDialog(self, initial_value=text, full_path=full_path).result
        
        #rename the item
        os.rename(full_path, new_path)

        #change the name of the item
        self.tree.item(item_id, text=new_name)

        #if the user entered a name, rename the item
        """if (new_name != text and new_name != None):
            #get the parent of the item
            parent_id = self.tree.parent(item_id)
            #get the index of the item
            index = self.tree.index(item_id)
            #rename the item
            self.tree.item(item_id, text=new_name)
            #remove the last item from the full path
            new_full_path = full_path.rsplit('/', 1)[0]
            #rename the file
            os.rename(full_path, new_full_path + '/' + new_name) """

    def _delete(self, item_id : str, full_path : str):
        #prompt the user to confirm the deletion
        confirm = tk.messagebox.askyesno("Delete", "Are you sure you want to permanently delete this item?")
        #if the user confirmed, delete the item
        if (confirm):
            #delete the item from the tree
            self.tree.delete(item_id)
            #delete the item from the filesystem
            os.remove(full_path)

    def _copy(self, item_id : str, full_path : str):
        pass

    def _cut(self, item_id : str, full_path : str):
        pass

    def _paste(self, item_id : str, full_path : str):
        pass
        
    def _change_backup_folder(self, item_id : str, full_path : str):
        pass

class RenameDialog(simpledialog.Dialog):
    def __init__(self, parent, initial_value, full_path):
        self.initial_value = initial_value

        if ('.' in initial_value):
            self.extensionless_name = initial_value.rsplit('.', 1)[0]
            self.extension = '.' + initial_value.rsplit('.', 1)[1]
        else:
            self.extensionless_name = initial_value
            self.extension = ''

        self.full_path = full_path

        super().__init__(parent, 'Rename Selected Item')

    def body(self, master):
        #set the default value of the entry to the current name
        self.entry = tk.Entry(master)
        self.entry.insert(0, self.extensionless_name)
        self.entry.grid(row=0, column=0)

        #Show the file extension if there is one
        self.extension_label = tk.Label(master, text=self.extension)
        self.extension_label.grid(row=0, column=1)
        
        #make the entry the default widget
        self.initial_focus = self.entry

        #get user input
        self.entry.bind("<Return>", lambda event: self.apply())

        return self.entry

    def apply(self):
        if (self.entry.get() == ''):
            self.result = self.initial_value, self.full_path
        else:
            self.result = self.entry.get() + self.extension, self.full_path.rsplit('/', 1)[0] + '/' + self.entry.get() + self.extension