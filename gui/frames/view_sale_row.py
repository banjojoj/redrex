import tkinter as tk
from customtkinter import CTkFrame, CTkLabel, CTkButton
from tkinter import ttk
from controller import sale_ctrl
from tkinter import messagebox


# Create TopView class inheriting CTkToplevel
class ViewSaleRow(CTkFrame):
    def __init__(self, master, item):
        super().__init__(master)
        self.master_tk_tree = master.tk_tree
        self.pack(anchor="n", fill="x", padx=15, pady=5, expand=True)

        self.values = item["values"]
        # Title Frame
        title_frame = CTkFrame(self, fg_color="transparent")
        title_frame.pack(padx=5, pady=5, fill="x", expand=True)

        # Configure grid columns to expand evenly
        for i in range(4):
            title_frame.grid_columnconfigure(i, weight=1)

        # Title Frame Elements
        CTkLabel(master=title_frame, text=f"{self.values[1]}", font=("Arial", 12)).grid(row=0, column=0, padx=5, sticky="w")
        CTkLabel(master=title_frame, text=f"{self.values[2]}", font=("Arial", 12)).grid(row=0, column=1, padx=5)
        CTkLabel(master=title_frame, text=f"{self.values[3]}", font=("Arial", 12)).grid(row=0, column=2, padx=5, sticky="e")

        close_button = CTkButton(title_frame, text="Close", fg_color="green", hover_color="#207244", font=("Arial Bold", 12), width=20, height=20, command=self.destroy)
        close_button.grid(row=0, column=3, sticky="e", padx=5, pady=5)

        # Create a Treeview widget to show the item details
        self.treeview = ttk.Treeview(self, columns=("Description", "Quantity", "Price", "Subtotal", "Serial No's"), show="headings")
        self.treeview.pack(fill="x", expand=False, padx=10, pady=(0, 10))

        # Define column headings
        self.treeview.heading(0, text="Description")
        self.treeview.heading(1, text="Quantity")
        self.treeview.heading(2, text="Price")
        self.treeview.heading(3, text="Subtotal")
        self.treeview.heading(4, text="Serial Nos")

        # Define tag styles for alternating row colors
        self.treeview.tag_configure("evenrow", background="light blue")  # Light Gray
        self.treeview.tag_configure("oddrow", background="white")  # White

        self.display_sales_details()

    def display_sales_details(self):
        details = sale_ctrl.get_sales_details(self.values[1])

        for i, sd in enumerate(details):
            data = (sd.get("product"), sd.get("quantity"), sd.get("price"), sd.get("sub_total"), sd.get("serial_nos"))
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.treeview.insert("", "end", iid=i, values=data, tags=(tag,))

