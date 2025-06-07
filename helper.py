"""Helper Functions"""
import customtkinter
from customtkinter import CTkLabel, CTkEntry, CTkComboBox
from controller import prod_ctrl, supp_ctrl, cust_ctrl, sale_ctrl
from tkinter import ttk, END, Scrollbar


def refresh_stripes(tree):
    """Refreshes the stripes of the treeview after modifying a treeview"""
    for index, item in enumerate(tree.get_children()):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.item(item, tags=(tag,))


def return_updated_products():
    """Function to Return Updated Products List"""
    all_rows = [{item.id: [item.description, item.type, item.cost, item.price, item.stock]} for item in prod_ctrl.get_prodby_desc()]
    return all_rows


def return_updated_suppliers():
    """Function to Return Updated Suppliers List"""
    all_rows = [{item.id: [item.name, item.address, item.tin_no, item.terms]} for item in supp_ctrl.get_all_supp()]
    return all_rows


def return_updated_customers():
    """Function to Return Updated Customers List"""
    all_rows = [{item.id: [item.name, item.address, item.tin_no, item.terms, item.balance]} for item in cust_ctrl.get_all_cust()]
    return all_rows


def return_updated_sales():
    """Function to Return Updated Sales List"""
    all_rows = [{item.id: [item.date, item.dr_si_no, item.customer.name, item.status, item.total]} for item in sale_ctrl.get_all_sales()]
    return all_rows


def compute_tree_total(tk_tree, total_label: customtkinter.CTkLabel):
    """Function to compute total sales based on Treeview"""
    total = 0.0

    for sale in tk_tree.get_children():
        row = tk_tree.item(sale, "values")
        total += float(row[-2])

    total_label.configure(text=f"Total: ${"{:,.2f}".format(total)}")


def compute_coll_total(tk_tree, total_label):
    """Function to compute total collections"""
    total = 0.0

    for coll in tk_tree.get_children():
        row = tk_tree.item(coll, "values")
        total += float(row[-1])

    total_label.configure(text=f"Total: ${"{:,.2f}".format(total)}")


def create_labeled_entry(master, label, row, column, width=145, entry_type="entry", **kwargs):
    """Function to dynamically create entries"""
    # Create Label
    entry_label = CTkLabel(master=master, text=label)
    entry_label.grid(sticky="w", row=row, column=column, padx=5, pady=5)

    # Create Entry
    if entry_type == "entry":
        entry = CTkEntry(master=master, width=width, border_color="#99BC85", border_width=2, **kwargs)
    else:
        entry = CTkComboBox(master=master, width=width, values=kwargs.get("values", []), command=kwargs.get("command"),
                            button_color="#99BC85", border_color="white", button_hover_color="#E4EFE7", border_width=2)
    entry.grid(sticky="w", row=row, column=column + 1, padx=5)
    return entry_label, entry


def create_select_treeview(tk_tree, name, list_names, frame):
    treeview_style = ttk.Style()
    treeview_style.configure("Custom.Treeview", rowheight=20, background="white", foreground="black", font=("Roboto", 10))
    treeview_style.configure("Custom.Treeview.Heading", background="gray", foreground="black", font=("Roboto", 10, "bold"))

    tk_tree.column("name", width=400, anchor="w")
    tk_tree.heading("name", text=f"{name}")

    # Insert Treeview
    for item in list_names:
        tk_tree.insert("", END, values=(item,))

    tk_tree.grid(row=1, column=1)
    scrollbar = Scrollbar(frame, command=tk_tree.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    tk_tree.configure(yscrollcommand=scrollbar.set)


def login_callback(username, password):
    """Placeholder for login callback function."""
    # Implement your login logic here
    if username == "admin" and password == "password":
        return True
    return False
