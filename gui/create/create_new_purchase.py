from customtkinter import *
import helper
from controller import supp_ctrl, prod_ctrl, purch_ctrl
from tkinter import ttk, Scrollbar, messagebox
from uuid import uuid4


class CreateNewPurchase(CTkFrame):
    def __init__(self, master, show_view, p_view):
        super().__init__(master)
        self.configure(fg_color="#fff")
        self.show_view = show_view
        self.p_view = p_view
        self.purch_tk_tree = p_view.tk_tree

        # Title Frame
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=15, pady=10)
        CTkLabel(master=title_frame, text="Create New Purchase", font=("Arial Black", 30), text_color="#99BC85").pack(anchor="w", side="left")

        self.save_button = CTkButton(master=title_frame, text="Save", fg_color="green", hover_color="#207244", font=("Arial Bold", 12), width=100, command=self.save_btn).pack(anchor="e", side="right", padx=15)
        self.back_button = CTkButton(master=title_frame, text="Back", fg_color="gray", hover_color="#207244", font=("Arial Bold", 12), width=100, command=lambda: show_view("PurchasesView")).pack(anchor="e", side="right")

        # ----------------- FIRST ROW -----------------
        first_row = CTkFrame(master=self, corner_radius=20)
        first_row.pack(fill="x", pady=10, padx=(50, 20), ipadx=25, ipady=20)

        # Receipt Frame
        receipt_frame = CTkFrame(master=first_row, fg_color="transparent")
        receipt_frame.pack(anchor="n", side="left", pady=(20, 0))
        self.dr_si_label, self.dr_si_entry = helper.create_labeled_entry(master=receipt_frame, label="DR/SI No:", row=0, column=0)
        self.date_label, self.date_entry = helper.create_labeled_entry(master=receipt_frame, label="Date:", row=1, column=0)
        self.status_label, self.status_entry = helper.create_labeled_entry(master=receipt_frame, label="Status:", row=2, column=0, entry_type="combo", values=["Ordered", "Posted", "Paid"])

        # Supplier Frame
        self.supplier_frame = CTkFrame(master=first_row, fg_color="transparent")
        self.supplier_frame.pack(anchor="n", side="left", padx=5, pady=(20, 0), expand=True)

        self.supplier_names = supp_ctrl.get_supp_names()
        self.supplier_label, self.supplier_entry = helper.create_labeled_entry(master=self.supplier_frame, label="Supplier:", row=0, column=0, width=320)
        self.supplier_entry.bind("<KeyRelease>", self.search_callback)
        self.supp_tree = ttk.Treeview(self.supplier_frame, columns=("name",), show="headings", height=10, style="Custom.Treeview")
        self.supp_tree.bind("<Double-1>", self.select_tree_callback)
        self.create_purch_treeview()

        # Product Frame
        self.product_frame = CTkFrame(master=first_row, fg_color="transparent")
        self.product_frame.pack(anchor="n", side="left", padx=5, pady=(20, 0), expand=True)

        self.product_names = prod_ctrl.get_prod_descs()
        self.product_label, self.product_entry = helper.create_labeled_entry(master=self.product_frame, label="Product:", row=0, column=0, width=320)
        self.product_entry.bind("<KeyRelease>", self.search_callback)
        self.prod_tree = ttk.Treeview(self.product_frame, columns=("name",), show="headings", height=10, style="Custom.Treeview")
        self.prod_tree.bind("<Double-1>", self.select_tree_callback)
        self.create_prod_treeview()

        # ----------------- SECOND ROW -----------------
        second_row = CTkFrame(master=self, fg_color="transparent")
        second_row.pack(side="left", pady=10, padx=(50, 0), anchor="nw")

        self.quantity_label, self.quantity_entry = helper.create_labeled_entry(master=second_row, label="Quantity:", row=0, column=0)
        self.price_label, self.price_entry = helper.create_labeled_entry(master=second_row, label="Price:", row=1, column=0)

        serial_frame = CTkFrame(master=second_row, fg_color="transparent")
        serial_frame.grid(row=2, column=0, sticky="w", columnspan=2, padx=5)
        CTkLabel(serial_frame, text="Serial No:", width=50).grid(row=2, column=0, sticky="w")
        self.serial_no_entry = CTkTextbox(master=serial_frame, fg_color="#F0F0F0", width=250, height=250, corner_radius=8)
        self.serial_no_entry.grid(row=4, column=0)

        # ----------------- THIRD ROW -----------------
        third_row = CTkFrame(master=self)
        third_row.pack(fill="both", padx=20)

        CTkLabel(third_row, text="Preview", width=50, font=("Arial Bold", 18)).pack(fill="x", side="top", pady=(20, 10))
        top_row = CTkFrame(master=third_row, fg_color="transparent")
        top_row.pack(fill="x", side="top", padx=10)
        self.dr_si_preview = CTkLabel(top_row, text=f"{self.dr_si_entry.get()}", width=50, anchor="w")
        self.dr_si_preview.grid(row=0, column=0, padx=(0, 50))
        self.dr_si_entry.bind("<KeyRelease>", command=lambda _: self.dr_si_preview.configure(text=f"{self.dr_si_entry.get()}"))

        self.supplier_preview = CTkLabel(top_row, text=f"{self.supplier_entry.get()}", width=50, anchor="e")
        self.supplier_preview.grid(row=0, column=1, padx=(50, 50))
        self.supplier_entry.bind("<KeyRelease>", command=lambda _: self.supplier_preview.configure(text=f"{self.supplier_entry.get()}"))

        self.date_preview = CTkLabel(top_row, text=f"{self.date_entry.get()}", width=50, anchor="w")
        self.date_preview.grid(row=1, column=0, padx=(0, 50))
        self.date_entry.bind("<KeyRelease>", command=lambda _: self.date_preview.configure(text=f"{self.date_entry.get()}"))

        bottom_row = CTkFrame(master=third_row, fg_color="transparent")
        bottom_row.pack(fill="x", side="bottom", padx=10)
        self.receipt_tree = ttk.Treeview(bottom_row, columns=("Product", "Quantity", "Price", "Subtotal", "Serial Number"), show="headings", height=10, style="Custom.Treeview")
        self.create_receipt_tree()
        self.receipt_tree.pack(fill="x", side="top")

        CTkButton(master=bottom_row, text="Add", fg_color="green", font=("Arial Bold", 12), width=100, command=self.add_btn).pack(side="right", pady=15, padx=10)
        CTkButton(master=bottom_row, text="Edit", fg_color="orange", font=("Arial Bold", 12), width=100, command=self.edit_btn).pack(side="right", pady=20, padx=10)
        CTkButton(master=bottom_row, text="Delete", fg_color="red", font=("Arial Bold", 12), width=100, command=self.delete_btn).pack(side="right", pady=20, padx=10)

        # Initialize Values
        self.all_products = []

    def create_purch_treeview(self):
        treeview_style = ttk.Style()
        treeview_style.configure("Custom.Treeview", rowheight=20, background="white", foreground="black", font=("Roboto", 10))
        treeview_style.configure("Custom.Treeview.Heading", background="gray", foreground="black", font=("Roboto",  10, "bold"))

        self.supp_tree.column("name", width=400, anchor="w")
        self.supp_tree.heading("name", text="Suppliers")

        # Insert Treeview
        for supplier in self.supplier_names:
            self.supp_tree.insert("", END, values=(supplier,))

        self.supp_tree.grid(row=1, column=1)
        scrollbar = Scrollbar(self.supplier_frame, command=self.supp_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.supp_tree.configure(yscrollcommand=scrollbar.set)

    def create_prod_treeview(self):
        treeview_style = ttk.Style()
        treeview_style.configure("Custom.Treeview", rowheight=20, background="white", foreground="black", font=("Roboto", 10))
        treeview_style.configure("Custom.Treeview.Heading", background="gray", foreground="black", font=("Roboto",  10, "bold"))

        self.prod_tree.column("name", width=400, anchor="w")
        self.prod_tree.heading("name", text="Products")

        # Insert Treeview
        for product in self.product_names:
            self.prod_tree.insert("", END, values=(product,))

        self.prod_tree.grid(row=1, column=1)
        scrollbar = Scrollbar(self.product_frame, command=self.prod_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.prod_tree.configure(yscrollcommand=scrollbar.set)

    def create_receipt_tree(self):
        # Define column headings and widths
        self.receipt_tree.heading("Product", text="Product")
        self.receipt_tree.column("Product", width=250)
        self.receipt_tree.heading("Quantity", text="Quantity")
        self.receipt_tree.column("Quantity", width=40, anchor="center")
        self.receipt_tree.heading("Price", text="Price")
        self.receipt_tree.column("Price", width=40, anchor="center")
        self.receipt_tree.heading("Subtotal", text="Subtotal")
        self.receipt_tree.column("Subtotal", width=40, anchor="center")
        self.receipt_tree.heading("Serial Number", text="Serial Number")
        self.receipt_tree.column("Serial Number", width=200)

    def search_callback(self, _):
        """Search on Product and Supplier Table"""
        supp_value = self.supplier_entry.get().lower()
        prod_value = self.product_entry.get().lower()

        # Clear existing Treeview data
        self.supp_tree.delete(*self.supp_tree.get_children())
        self.prod_tree.delete(*self.prod_tree.get_children())

        # Filter rows based on search
        supp_filtered_rows = []
        for item in self.supplier_names:
            if supp_value in item.lower():
                supp_filtered_rows.append(item)

        prod_filtered_rows = []
        for item in self.product_names:
            if prod_value in item.lower():
                prod_filtered_rows.append(item)

        # Manually Repopulate the tree with filtered data
        if supp_value != "":
            for index, item in enumerate(supp_filtered_rows):
                self.supp_tree.insert("", "end", iid=index, values=(item,))
        else:
            for index, item in enumerate(self.supplier_names):
                self.supp_tree.insert("", "end", iid=index, values=(item,))

        if prod_value != "":
            for index, item in enumerate(prod_filtered_rows):
                self.prod_tree.insert("", "end", iid=index, values=(item,))
        else:
            for index, item in enumerate(self.product_names):
                self.prod_tree.insert("", "end", iid=index, values=(item,))

    def select_tree_callback(self, _):
        """Autocomplete supplier and product entry on double click"""
        supp_selected = self.supp_tree.focus()
        prod_selected = self.prod_tree.focus()
        if supp_selected:
            values = self.supp_tree.item(supp_selected, "values")
            self.supplier_entry.delete(0, END)
            self.supplier_entry.insert(0, values[0])

            self.supplier_preview.configure(text=f"{values[0]}")

        if prod_selected:
            values = self.prod_tree.item(prod_selected, "values")
            self.product_entry.delete(0, END)
            self.product_entry.insert(0, values[0])

    def add_btn(self):
        product = {
            "product": self.product_entry.get(), "quantity": self.quantity_entry.get(), "price": self.price_entry.get(), "sub_total": None, "serial_no": self.serial_no_entry.get("0.0", "end-1c")
        }

        # Check Entries
        if "" in [product.get("product"), product.get("quantity"), product.get("price")]:
            messagebox.showerror(title="Error!", message="Missing values in product, quantity, or price")
        else:
            try:
                sub_total = int(product.get("quantity")) * float(product.get("price"))
            except ValueError:
                messagebox.showerror(title="Error!", message="Quantity or Price must be a number.")
            else:
                product["sub_total"] = sub_total
                product["quantity"] = int(product.get("quantity"))
                product["price"] = float(product.get("price"))
                self.all_products.append(product)
                # Insert to treeview
                self.show_receipt_rows()
                self.clear_entries()

    def edit_btn(self):
        selected_item = self.receipt_tree.selection()

        if len(selected_item) == 1:
            values = self.receipt_tree.item(selected_item[0], "values")
            self.clear_entries()
            # Insert to Entries
            self.product_entry.insert(0, values[0])
            self.quantity_entry.insert(0, values[1])
            self.price_entry.insert(0, values[2])
            self.serial_no_entry.insert("end", values[4])

            # Remove from treeview and products list
            for product in self.all_products:
                if product.get("product") == values[0]:
                    self.all_products.remove(product)

            self.show_receipt_rows()

        else:
            messagebox.showerror("Error!", "Possible Reasons:\n-Select only 1 (one) record to edit.\n-No record selected.")

    def delete_btn(self):
        selected_items = self.receipt_tree.selection()

        for item in selected_items:
            values = self.receipt_tree.item(item, "values")
            for product in self.all_products:
                if product.get("product") == values[0]:
                    self.all_products.remove(product)

        self.show_receipt_rows()

    def save_btn(self):
        pass

    def show_receipt_rows(self):
        self.receipt_tree.delete(*self.receipt_tree.get_children())
        # Insert to treeview
        for index, product in enumerate(self.all_products):
            values = (product.get("product"), product.get("quantity"), product.get("price"), product.get("sub_total"), product.get("serial_no"))
            self.receipt_tree.insert("", END, values=values)

    def clear_entries(self, include_receipt=False):
        if include_receipt:
            # Clear Products List
            self.all_products = None
            self.dr_si_entry.delete(0, END)
            self.date_entry.delete(0, END)
            self.status_entry.set('')
            self.supplier_entry.delete(0, END)

        # Clear Entries for Products
        self.product_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.serial_no_entry.delete("0.0", "end")

