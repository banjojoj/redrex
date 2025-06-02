from tkinter import *
from tkinter import ttk
from controller import prod_ctrl, supp_ctrl, cust_ctrl, sale_ctrl, purch_ctrl, coll_ctrl


class Treeview:

    def __init__(self, root, columns):
        # Initialize Frame
        self.root = root

        # Create Scrollbar
        table_scrollbar = Scrollbar(self.root)
        table_scrollbar.pack(side=RIGHT, fill=Y)

        # Add Style to Treeview
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", rowheight=20, background="white", foreground="black", font=("Roboto", 9))
        self.style.configure("Custom.Treeview.Heading", background="gray", foreground="black", font=("Roboto",  10, "bold"))

        # Define Treeview
        self.treeview = ttk.Treeview(self.root, yscrollcommand=table_scrollbar.set, style="Custom.Treeview", show="headings")
        # Define tag styles for alternating row colors
        self.treeview.tag_configure("evenrow", background="#E4EFE7")
        self.treeview.tag_configure("oddrow", background="white")

        self.treeview.pack(fill="both", expand=True)

        # Configure Scrollbar
        table_scrollbar.config(command=self.treeview.yview)

        # Define Columns
        self.treeview['columns'] = columns

        # Show Headings
        for index in range(len(columns)):
            self.treeview.heading(columns[index], text=columns[index])

    def show_products(self, sort):
        # Refresh Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Edit Headings
        self.treeview.column("Description", width=550)
        self.treeview.column("Cost", anchor="e")
        self.treeview.column("Price", anchor="e")
        self.treeview.column("Stock", anchor="e")

        # Sort Rows based on sort parameter
        if sort == "Description":
            products = prod_ctrl.get_prodby_desc()
        else:
            products = prod_ctrl.get_prodby_type()

        for i, p in enumerate(products):
            data = (p.description, p.type, p.cost, p.price, p.stock)
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.treeview.insert("", "end", iid=p.id, values=data, tags=(tag,))

    def show_suppliers(self):
        # Refresh Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Edit Headings
        self.treeview.column("Name", width=400)
        self.treeview.column("Address", width=550)
        self.treeview.column("TIN-No", width=100, anchor="center")
        self.treeview.column("Terms", width=100, anchor="center")

        suppliers = supp_ctrl.get_all_supp()
        for i, s in enumerate(suppliers):
            data = (s.name, s.address, s.tin_no, s.terms)
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.treeview.insert("", "end", iid=s.id, values=data, tags=(tag,))

    def show_customers(self):
        # Refresh Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Edit Headings
        self.treeview.column("Name", width=400)
        self.treeview.column("Address", width=510)
        self.treeview.column("TIN-No", width=120, anchor="center")
        self.treeview.column("Terms", width=120, anchor="center")
        self.treeview.column("Balance", width=120, anchor="e")

        customers = cust_ctrl.get_all_cust()
        for i, c in enumerate(customers):
            data = (c.name, c.address, c.tin_no, c.terms, c.balance)
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.treeview.insert("", "end", iid=c.id, values=data, tags=(tag,))

    def show_sales(self):
        # Refresh Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Edit Headings
        self.treeview.column("Date", anchor="center")
        self.treeview.column("Customer", width=510)
        self.treeview.column("Total", anchor="e")
        self.treeview.column("Status", anchor="center")

        sales = sale_ctrl.get_sales_rows()
        for i, s in enumerate(sales):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.treeview.insert("", "end", iid=s[0], values=s[1:], tags=(tag,))

    def show_purchases(self):
        # Refresh Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Edit Headings
        self.treeview.column("Date", anchor="center")
        self.treeview.column("Supplier", width=510)
        self.treeview.column("Total", anchor="e")
        self.treeview.column("Status", anchor="center")

        purchases = purch_ctrl.get_all_purchases()
        for i, p in enumerate(purchases):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            for iid, values in p.items():
                self.treeview.insert("", "end", iid=iid, values=values, tags=(tag,))

    def show_collections(self):
        # Refresh Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Edit Headings
        self.treeview.column("Date", anchor="center")
        self.treeview.column("Customer", width=510)
        self.treeview.column("DR/SI No", anchor="center")
        self.treeview.column("Amount", anchor="e")

        collection = coll_ctrl.get_all_collections()
        for i, c in enumerate(collection):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            for iid, values in c.items():
                self.treeview.insert("", "end", iid=iid, values=values, tags=(tag,))









