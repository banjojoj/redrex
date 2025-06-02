from customtkinter import CTkFrame, CTkLabel, CTkButton
from gui.treeview import Treeview
from gui.tabs.purch_tab import PurchasesTabView
from tkinter import Menu
from gui.frames.view_sale_row import ViewSaleRow
import helper
from controller import purch_ctrl


class PurchasesView(CTkFrame):
    def __init__(self, master, show_view):
        super().__init__(master)
        self.configure(fg_color="#fff")

        # Initialize Treeview
        self.tree_frame = CTkFrame(master=self, fg_color="transparent")
        columns = ("Date", "DR/SI No", "Supplier", "Total", "Status")
        self.tree = Treeview(root=self.tree_frame, columns=columns)
        self.tree.show_purchases()

        self.tk_tree = self.tree.treeview
        self.tk_tree.bind("<Button-3>", self.show_row_menu)
        # Get All Rows From Treeview
        self.all_rows = [{item: self.tk_tree.item(item)["values"]} for item in self.tk_tree.get_children()]

        # Title Frame
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=15, pady=10)
        CTkLabel(master=title_frame, text="Purchases", font=("Arial Black", 30), text_color="#99BC85").pack(anchor="w", side="left")

        self.new_purch_button = CTkButton(master=title_frame, text="+ New Purchase", fg_color="green", hover_color="#207244", font=("Arial Bold", 12), width=100,  command=lambda: show_view("CreateNewPurchase"))
        self.new_purch_button.pack(anchor="e", side="right", padx=15)

        self.total = 0.0
        self.total_label = CTkLabel(master=title_frame, text=f"Total: ${self.total}", font=("Arial Black", 15), text_color="#2A8C55")
        self.total_label.pack(anchor="e", side="right", padx=(0, 20))

        # Create Filter TabView
        self.purch_tab_view = PurchasesTabView(self)
        self.purch_tab_view.pack(fill="x", padx=15)

        # Pack Treeview Frame and Compute Total
        self.tree_frame.pack(fill="both", expand=True, padx=15, pady=10)
        helper.compute_tree_total(self.tk_tree, self.total_label)

        # Get Current ViewSaleRow if any
        self.view_sale_row = None

    def show_row_menu(self, event):
        """Callback function on right click in Treeview Row"""
        # Get selected item
        item = self.tk_tree.identify('item', event.x, event.y)

        # Focus on the row
        self.tk_tree.selection_set(item)
        self.tk_tree.focus(item)

        # Create menu
        context_menu = Menu(self, tearoff=0)
        context_menu.add_command(label="View", command=lambda: print("Option 1 selected"))
        context_menu.add_command(label="Edit", command=lambda: print("Option 2 selected"))
        context_menu.add_command(label="Delete", command=lambda: print("Option 3 selected"))

        # Display the context menu at the mouse cursor position
        context_menu.post(event.x_root, event.y_root)