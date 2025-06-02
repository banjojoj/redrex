from customtkinter import CTkFrame, CTkLabel, CTkComboBox, END
from gui.treeview import Treeview
from gui.tabs.coll_tab import CollectionTabView
from tkinter import Menu
from controller import prod_ctrl
import helper


class CollectionView(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#fff", corner_radius=0)

        # Initialize Treeview
        tree_frame = CTkFrame(master=self, fg_color="transparent")
        columns = ("Date", "Customer", "DR/SI No", "Amount")
        self.tree = Treeview(root=tree_frame, columns=columns)
        self.tree.show_collections()

        self.tk_tree = self.tree.treeview
        self.tk_tree.bind("<Button-3>", self.show_row_menu)
        # Get All Rows From Treeview
        self.all_rows = [{item: self.tk_tree.item(item)["values"]} for item in self.tk_tree.get_children()]

        # Title Frame
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=15, pady=10)
        CTkLabel(master=title_frame, text="Collections", font=("Arial Black", 30), text_color="#99BC85").pack(anchor="w", side="left")

        self.total = 0.0
        self.total_label = CTkLabel(master=title_frame, text=f"Total: ${self.total}", font=("Arial Black", 15), text_color="#2A8C55")
        self.total_label.pack(anchor="e", side="right", padx=(0, 20))

        # Create Filter TabView
        self.product_tabview = CollectionTabView(self)
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
        context_menu.add_command(label="Edit", command=lambda: print("Option 1"))
        context_menu.add_command(label="Delete", command=lambda: print("Option 2"))

        # Display the context menu at the mouse cursor position
        context_menu.post(event.x_root, event.y_root)

    def delete_coll(self, item):
        # sale_ctrl.delete_sale(item)

        # Delete Row and Refresh Stripes of Treeview
        self.tk_tree.delete(item)
        helper.refresh_stripes(self.tk_tree)

        # Update Products List in Product Tab
        # self.sales_tab_view.all_rows = sale_ctrl.get_all_sales()






















