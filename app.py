import tkinter as tk
from tkinter import ttk

import os

#Since tkinter filedialogs are derived from the OS,
#they cannot be embedded in a tkinter window. I will therefore have to make my own tkinter-based file browser.
#I will use the treeview widget to do this.


class TKFileBrowser(tk.Tk):
    def __init__(self, root : str, width : int, height : int):
        super().__init__()
        self.title("File Browser")
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

        #list of directories
        self.directories = []
        self.root_name = root
        self._initialize_tree()

    def _initialize_tree(self):
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.heading("#0", text=self.root_name, anchor=tk.W)
        root_node = self.tree.insert("", tk.END, text=self.root_name, open=True)

        self.populate_tree(self.root_name, root_node, self.root_name)

        self.tree.bind("<Double-Button-1>", self.on_double_click)
        #self.tree.bind("<Button-3>", self.on_right_click) 

    def populate_tree(self, dir_name : str, dir_id : str, full_path : str = None):
        #add the files and directories but ignore hidden ones
        contents = [file for file in self.search_directory(full_path) if not file.startswith(".")]

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
                self.directories.append(full_path)

            index += 1

    def search_directory(self, dir : str):
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

    def on_double_click(self, event):
        #get the item that was clicked
        item_id = self.tree.selection()[0]

        #get the text of the item
        item_text = self.tree.item(item_id, "text")

        full_path = self._get_full_path(item_id, item_text)

        #if the item is a directory, open it
        if (full_path in self.directories):
            #populate the directory
            self.populate_tree(item_text, item_id, full_path)
            #open the directory
            self.tree.item(item_id, open=True)

if __name__ == "__main__":
    root = "/home/jackson"
    width = 500
    height = 500

    app = TKFileBrowser(root, width, height)
    app.mainloop()