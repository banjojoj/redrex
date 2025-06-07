from customtkinter import *
import helper
from controller import cust_ctrl, coll_ctrl, sale_ctrl
from tkinter import ttk, Scrollbar, messagebox
from uuid import uuid4


class CreateNewCollection(CTkFrame):
    def __init__(self, master, show_view, c_view):
        super().__init__(master)
        self.configure(fg_color="#fff")
        self.show_view = show_view
        self.c_view = c_view
        self.coll_tk_tree = c_view.tk_tree

        # Title Frame
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=15, pady=10)
        CTkLabel(master=title_frame, text="Create New Collection", font=("Arial Black", 30), text_color="#99BC85").pack(anchor="w", side="left")

        self.save_button = CTkButton(master=title_frame, text="Save", fg_color="green", hover_color="#207244", font=("Arial Bold", 12), width=100, command=self.save_btn).pack(anchor="e", side="right", padx=15)
        self.back_button = CTkButton(master=title_frame, text="Back", fg_color="gray", hover_color="#207244", font=("Arial Bold", 12), width=100, command=lambda: show_view("CollectionView")).pack(anchor="e", side="right")

        # ----------------- FIRST ROW -----------------
        first_row = CTkFrame(master=self, corner_radius=20)
        first_row.pack(fill="x", pady=10, padx=(50, 20), ipadx=25, ipady=20)

        # Receipt Frame
        receipt_frame = CTkFrame(master=first_row, fg_color="transparent")
        receipt_frame.pack(anchor="n", side="left", pady=(20, 0))

        self.date_label, self.date_entry = helper.create_labeled_entry(master=receipt_frame, label="Date:", row=0, column=0, width=120)
        self.amt_label, self.amt_entry = helper.create_labeled_entry(master=receipt_frame, label="Amount:", row=1, column=0, width=120)
        self.remarks_label, self.remarks_entry = helper.create_labeled_entry(master=receipt_frame, entry_type="combo", values=["CASH", "CHECK"], label="Remarks:", row=2, column=0, width=120)
        self.bank_label, self.bank_entry = helper.create_labeled_entry(master=receipt_frame, label="Bank Type:", row=3, column=0, width=120)
        self.check_no_label, self.check_no_entry = helper.create_labeled_entry(master=receipt_frame, label="Check No:", row=0, column=3, width=120)
        self.check_date_label, self.check_date_entry = helper.create_labeled_entry(master=receipt_frame, label="Check Date:", row=1, column=3, width=120)

        # Customer Frame
        self.customer_frame = CTkFrame(master=first_row, fg_color="transparent")
        self.customer_frame.pack(anchor="n", side="left", padx=5, pady=(20, 0), expand=True)

        self.customer_names = cust_ctrl.get_cust_names()
        self.customer_label, self.customer_entry = helper.create_labeled_entry(master=self.customer_frame, label="Customer:", row=0, column=0, width=320)
        self.customer_entry.bind("<KeyRelease>", self.search_callback)
        self.cust_tree = ttk.Treeview(self.customer_frame, columns=("name",), show="headings", height=10, style="Custom.Treeview")
        self.cust_tree.bind("<Double-1>", self.select_tree_callback)
        self.create_cust_treeview()

        # Dr/SI Frame
        self.drsi_frame = CTkFrame(master=first_row, fg_color="transparent")
        self.drsi_frame.pack(anchor="n", side="left", padx=5, pady=(20, 0), expand=True)

        self.drsi_values = sale_ctrl.get_drsi_values()
        self.drsi_label, self.drsi_entry = helper.create_labeled_entry(master=self.drsi_frame, label="DR/SI:", row=0, column=0, width=320)
        self.drsi_entry.bind("<KeyRelease>", self.search_callback)
        self.drsi_tree = ttk.Treeview(self.drsi_frame, columns=("name",), show="headings", height=10, style="Custom.Treeview")
        self.drsi_tree.bind("<Double-1>", self.select_tree_callback)
        self.create_drsi_tree()

    def search_callback(self, _):
        """Search Customer Table"""
        cust_value = self.customer_entry.get().lower()
        drsi_value = self.drsi_entry.get().lower()

        # Clear existing Treeview data
        self.cust_tree.delete(*self.cust_tree.get_children())
        self.drsi_tree.delete(*self.drsi_tree.get_children())

        # Filter rows based on search
        cust_filtered_rows = []
        for item in self.customer_names:
            if cust_value in item.lower():
                cust_filtered_rows.append(item)

        drsi_filtered_rows = []
        for item in self.drsi_values:
            if drsi_value in item.lower():
                drsi_filtered_rows.append(item)

        # Manually Repopulate the tree with filtered data
        if cust_value != "":
            for index, item in enumerate(cust_filtered_rows):
                self.cust_tree.insert("", "end", iid=index, values=(item,))
        else:
            for index, item in enumerate(self.customer_names):
                self.cust_tree.insert("", "end", iid=index, values=(item,))

        if drsi_value != "":
            for index, item in enumerate(drsi_filtered_rows):
                self.drsi_tree.insert("", "end", iid=index, values=(item,))
        else:
            for index, item in enumerate(self.drsi_values):
                self.drsi_tree.insert("", "end", iid=index, values=(item,))

    def select_tree_callback(self, _):
        """Autocomplete customer entry on double click"""
        cust_selected = self.cust_tree.focus()
        if cust_selected:
            values = self.cust_tree.item(cust_selected, "values")
            self.customer_entry.delete(0, END)
            self.customer_entry.insert(0, values[0])

            # self.supplier_preview.configure(text=f"{values[0]}")

    def create_cust_treeview(self):
        treeview_style = ttk.Style()
        treeview_style.configure("Custom.Treeview", rowheight=20, background="white", foreground="black", font=("Roboto", 10))
        treeview_style.configure("Custom.Treeview.Heading", background="gray", foreground="black", font=("Roboto",  10, "bold"))

        self.cust_tree.column("name", width=400, anchor="w")
        self.cust_tree.heading("name", text="Customers")

        # Insert Treeview
        for customer in self.customer_names:
            self.cust_tree.insert("", END, values=(customer,))

        self.cust_tree.grid(row=1, column=1)
        scrollbar = Scrollbar(self.customer_frame, command=self.cust_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.cust_tree.configure(yscrollcommand=scrollbar.set)

    def create_drsi_tree(self):
        treeview_style = ttk.Style()
        treeview_style.configure("Custom.Treeview", rowheight=20, background="white", foreground="black", font=("Roboto", 10))
        treeview_style.configure("Custom.Treeview.Heading", background="gray", foreground="black", font=("Roboto",  10, "bold"))

        self.drsi_tree.column("name", width=400, anchor="w")
        self.drsi_tree.heading("name", text="DR/SI Nos")

        # Insert Treeview
        for drsi in self.drsi_values:
            self.drsi_tree.insert("", END, values=(drsi,))

        self.drsi_tree.grid(row=1, column=1)
        scrollbar = Scrollbar(self.drsi_frame, command=self.drsi_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.drsi_tree.configure(yscrollcommand=scrollbar.set)

    def save_btn(self):
        details = {
            "date": self.date_entry.get(), "amount": self.amt_entry.get(),
            "remarks": self.remarks_entry.get(), "bank_type": self.bank_entry.get(),
            "check_no": self.check_no_entry.get(), "check_date": self.check_date_entry.get(),
            "customer": self.customer_entry.get(), "dr_si_no": self.drsi_entry.get()
        }

        if not all(details.values()):
            messagebox.showerror("Error", "Please fill all fields")
        else:
            # Add to Database
            coll_iid = str(uuid4())[:6]
            date = details["date"]
            amount = float(details["amount"])
            remarks = details["remarks"]
            bank_type = details["bank_type"]
            check_no = details["check_no"]
            check_date = details["check_date"]
            customer = details["customer"]
            dr_si_no = details["dr_si_no"]
            customer_id = cust_ctrl.get_cust_id(customer)
            sales_id = sale_ctrl.get_sales_id(dr_si_no)

            coll_ctrl.create_collection(
                iid=coll_iid, date=date, customer_name=customer, dr_si_no=dr_si_no,
                amount=amount, remarks=remarks, bank_type=bank_type, check_no=check_no,
                check_date=check_date, sales_id=sales_id, customer_id=customer_id
            )

            # Update Sales Status
            sale_ctrl.update_sales_status(dr_si_no, "Paid")

            # Show in Main Treeview
            values = (date, customer, dr_si_no, amount)
            self.coll_tk_tree.insert("", "end", iid=coll_iid, values=values)
            helper.refresh_stripes(self.coll_tk_tree)

            # Update all rows
            self.c_view.all_rows = coll_ctrl.get_all_collections()
            self.show_view("CollectionView")
