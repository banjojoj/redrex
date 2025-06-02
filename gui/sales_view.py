from customtkinter import CTkFrame, CTkLabel, CTkButton
from gui.treeview import Treeview
from gui.tabs.sale_tab import SalesTabView
from tkinter import Menu
from gui.frames.view_sale_row import ViewSaleRow
import helper
from controller import sale_ctrl


class SalesView(CTkFrame):
    def __init__(self, master, show_view):
        super().__init__(master)
        self.configure(fg_color="#fff")

        # Initialize Treeview
        self.tree_frame = CTkFrame(master=self, fg_color="transparent")
        columns = ("Date", "DR/SI No", "Customer", "Total", "Status")
        self.tree = Treeview(root=self.tree_frame, columns=columns)
        self.tree.show_sales()

        self.tk_tree = self.tree.treeview
        self.tk_tree.bind("<Button-3>", self.show_row_menu)
        # Get All Rows From Treeview
        self.all_rows = [{item: self.tk_tree.item(item)["values"]} for item in self.tk_tree.get_children()]

        # Title Frame
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=15, pady=10)
        CTkLabel(master=title_frame, text="Sales", font=("Arial Black", 30), text_color="#99BC85").pack(anchor="w", side="left")

        self.new_sale_button = CTkButton(master=title_frame, text="+ New Sale", fg_color="green", hover_color="#207244", font=("Arial Bold", 12), width=100, command=lambda: show_view("CreateNewSale"))
        self.new_sale_button.pack(anchor="e", side="right", padx=15)

        self.total = 0.0
        self.total_label = CTkLabel(master=title_frame, text=f"Total: ${self.total}", font=("Arial Black", 15), text_color="#2A8C55")
        self.total_label.pack(anchor="e", side="right", padx=(0, 20))

        # Create Filter TabView
        self.sales_tab_view = SalesTabView(self)
        self.sales_tab_view.pack(fill="x", padx=15)

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
        context_menu.add_command(label="View", command=lambda: self.show_view_sale(item=self.tk_tree.item(item)))
        context_menu.add_command(label="Edit", command=lambda: print("Option 2 selected"))
        context_menu.add_command(label="Delete", command=lambda: self.delete_sale(item=item))

        # Display the context menu at the mouse cursor position
        context_menu.post(event.x_root, event.y_root)

    def show_view_sale(self, item):
        """Function to Toggle ViewSaleRow Frame"""
        if self.view_sale_row:
            self.view_sale_row.destroy()
        self.view_sale_row = ViewSaleRow(master=self, item=item)

    def delete_sale(self, item):
        # Delete Row and Refresh Stripes of Treeview
        sale_ctrl.delete_sale(item)
        self.tk_tree.delete(item)       # Remove row from treeview
        helper.refresh_stripes(self.tk_tree)

        # Update Products List in Product Tab
        self.sales_tab_view.all_rows = sale_ctrl.get_all_sales()
