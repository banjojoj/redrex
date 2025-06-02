from customtkinter import CTkFrame, CTkLabel
from gui.treeview import Treeview
from gui.tabs.supp_tab import SupplierTabView
from tkinter import Menu
from controller import supp_ctrl
import helper


class SupplierView(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#fff")

        # Initialize Treeview
        tree_frame = CTkFrame(master=self, fg_color="transparent")
        columns = ("Name", "Address", "TIN-No", "Terms")
        self.tree = Treeview(root=tree_frame, columns=columns)
        self.tree.show_suppliers()

        self.tk_tree = self.tree.treeview
        self.tk_tree.bind("<Button-3>", self.show_row_menu)
        # Get All Rows From Treeview
        self.all_rows = [{item: self.tk_tree.item(item)["values"]} for item in self.tk_tree.get_children()]

        # Title Frame
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=15, pady=10)
        CTkLabel(master=title_frame, text="Supplier", font=("Arial Black", 30), text_color="#99BC85").pack(anchor="nw", side="left")

        # Create Filter TabView
        self.supplier_tabview = SupplierTabView(self)
        self.supplier_tabview.pack(fill="x", padx=15)

        # Pack Treeview Frame
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

    def show_row_menu(self, event):
        """Callback function on right click in Treeview Row"""
        # Get selected item
        item = self.tk_tree.identify('item', event.x, event.y)

        # Focus on the row
        self.tk_tree.selection_set(item)
        self.tk_tree.focus(item)

        # Create menu
        context_menu = Menu(self, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: print("Option 1 selected"))
        context_menu.add_command(label="Delete", command=lambda: self.delete_supp(item))

        # Display the context menu at the mouse cursor position
        context_menu.post(event.x_root, event.y_root)

    def delete_supp(self, item):
        # Delete Row and Refresh Stripes of Treeview
        supp_ctrl.delete_supp(item)
        self.tk_tree.delete(item)       # Remove row from treeview
        helper.refresh_stripes(self.tk_tree)

        # Update Supplier List in Supplier Tab
        self.supplier_tabview.all_rows = helper.return_updated_suppliers()
