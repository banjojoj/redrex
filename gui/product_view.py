from customtkinter import CTkFrame, CTkLabel, CTkComboBox, END
from gui.treeview import Treeview
from gui.tabs.prod_tab import ProductTabView
from tkinter import Menu
from controller import prod_ctrl
import helper


class ProductView(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#fff", corner_radius=0)

        # Initialize Treeview
        tree_frame = CTkFrame(master=self, fg_color="transparent")
        columns = ("Description", "Type", "Cost", "Price", "Stock")
        self.tree = Treeview(root=tree_frame, columns=columns)
        self.tree.show_products("Description")      # Initially show Products by Description

        self.tk_tree = self.tree.treeview
        self.tk_tree.bind("<Button-3>", self.show_row_menu)
        # Get All Rows From Treeview
        self.all_rows = [{item: self.tk_tree.item(item)["values"]} for item in self.tk_tree.get_children()]

        # Title Frame
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=15, pady=10)
        CTkLabel(master=title_frame, text="Products", font=("Arial Black", 30), text_color="#99BC85").pack(anchor="w", side="left")

        # Create Filter TabView
        self.product_tabview = ProductTabView(self)
        self.product_tabview.pack(fill="x", padx=15)

        # Pack Treeview Frame
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Current Rows for Editing
        self.current_rows = None

    def show_row_menu(self, event):
        """Callback function on right click in Treeview Row"""
        # Get selected item
        item = self.tk_tree.identify('item', event.x, event.y)

        # Focus on the row
        self.tk_tree.selection_set(item)
        self.tk_tree.focus(item)

        # Create menu
        context_menu = Menu(self, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: self.edit_product(item))
        context_menu.add_command(label="Delete", command=lambda: self.delete_prod(item))

        # Display the context menu at the mouse cursor position
        context_menu.post(event.x_root, event.y_root)

    def delete_prod(self, item):
        # Delete Row and Refresh Stripes of Treeview
        prod_ctrl.delete_prod(item)
        self.tk_tree.delete(item)       # Remove row from treeview
        helper.refresh_stripes(self.tk_tree)

        # Update Products List in Product Tab
        self.product_tabview.all_rows = helper.return_updated_products()

    def edit_product(self, item):
        # Set tab to Create and Get the values of the row
        self.product_tabview.set("Create")
        values = self.tk_tree.item(item, "values")

        # Add rows to entries
        entries = self.product_tabview.return_entries()

        # Clear Entries
        for entry in entries:
            if isinstance(entry, CTkComboBox):
                entry.set('')
            else:
                entry.delete(0, END)

        # Insert Values to Create Entries
        for i in range(len(entries)):
            entry = entries[i]
            value = values[i]
            if isinstance(entry, CTkComboBox):
                entry.set('')
                entry.set(values[1])
            else:
                entry.insert(0, value)
