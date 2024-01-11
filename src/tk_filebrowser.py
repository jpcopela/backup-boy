import tkinter as tk
from tkinter import ttk

import os

#Since tkinter filedialogs are derived from the OS, they cannot be embedded in a tkinter window. 
#I will therefore have to make my own tkinter-based file browser using a treeview widget.
class TKFileBrowser(tk.Frame):
    def __init__(self, root : str):
        super().__init__()

        #list of directories
        self.directories = []
        self.root_name = root
        self._initialize_tree()

    #initialize the treeview widget and populate the root directory
    def _initialize_tree(self):
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.folder_icon = tk.PhotoImage(file="resources/icons/empty_folder.png")
    
        self.tree.heading("#0", text=self.root_name, anchor=tk.W)
        root_node = self.tree.insert("", tk.END, text=self.root_name, open=True)

        self._populate_tree(self.root_name, root_node, self.root_name)

        self.tree.bind("<Double-Button-1>", self._on_double_click)
        self.tree.bind("<Button-3>", self._on_right_click) 

    #populate the tree with the contents of a directory
    def _populate_tree(self, dir_name : str, dir_id : str, full_path : str = None):
        #add the files and directories but ignore hidden ones
        contents = [file for file in self._search_directory(full_path) if not file.startswith(".")]

        #variable for storing the index of the node
        index = 0

        #add the contents to the tree
        for item in contents:
            item_id = self.tree.insert(dir_id, index, text=item)

            #get the full path of the item
            full_path = self._get_full_path(item_id, item)
            #add the item to the tree
            #if the item is a directory, log it
            if os.path.isdir(full_path):
                self.tree.item(item_id, image=self.folder_icon)
                self.directories.append(full_path)

            index += 1

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

    def _on_double_click(self, event):
        #get the item that was clicked
        item_id = self.tree.selection()[0]

        #get the text of the item
        item_text = self.tree.item(item_id, "text")

        full_path = self._get_full_path(item_id, item_text)

        #if the item is a directory, open it
        if (full_path in self.directories):
            #populate the directory
            self._populate_tree(item_text, item_id, full_path)
            #open the directory
            self.tree.item(item_id, text=item_text, open=True)

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
        menu.add_command(label="Rename", command=lambda: self._rename(item_id, item_text, full_path))
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

    def _rename(self, item_id : str, item_text : str, full_path : str):
        pass

    def _delete(self, item_id : str, full_path : str):
        pass

    def _copy(self, item_id : str, full_path : str):
        pass

    def _cut(self, item_id : str, full_path : str):
        pass

    def _paste(self, item_id : str, full_path : str):
        pass
        
    def _change_backup_folder(self, item_id : str, full_path : str):
        pass