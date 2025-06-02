from customtkinter import CTkTabview, CTkEntry, CTkLabel, CTkComboBox, CTkButton, END
from controller import supp_ctrl
from tkinter import messagebox
from uuid import uuid4
import helper


class SupplierTabView(CTkTabview):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Configure TabView Style
        self.configure(height=130, segmented_button_fg_color="#99BC85", segmented_button_selected_color="#E4EFE7", segmented_button_selected_hover_color="#E4EFE7", segmented_button_unselected_hover_color="#E4EFE7",
                       segmented_button_unselected_color="#99BC85", text_color="black", text_color_disabled="black", anchor="nw")
        self._segmented_button.configure(font=("Arial Bold", 12), corner_radius=5)

        # Add Tabs
        table_tab = self.add("Table")
        create_tab = self.add("Create")

        # Initialize Table Tab
        CTkLabel(master=table_tab, text="Search:").pack(side="left", anchor="w", padx=5, pady=5)
        self.search = CTkEntry(master=table_tab, width=305, placeholder_text="Search Supplier...", border_color="#99BC85", border_width=2)
        self.search.bind("<KeyRelease>", self.search_callback)
        self.search.pack(side="left", anchor="w", padx=5, pady=5)

        # Initialize Create Tab
        # First Row
        CTkLabel(master=create_tab, text="Supplier:").grid(sticky="w", row=0, column=0, padx=5, pady=5)
        self.name_entry = CTkEntry(master=create_tab, width=305, border_color="#2A8C55", border_width=2)
        self.name_entry.grid(sticky="w", row=0, column=1, padx=5)

        CTkLabel(master=create_tab, text="Address:").grid(sticky="w", row=0, column=2, padx=5)
        self.address_entry = CTkEntry(master=create_tab, width=305, border_color="#2A8C55", border_width=2)
        self.address_entry.grid(sticky="w", row=0, column=3, padx=5)

        CTkLabel(master=create_tab, text="TIN No:").grid(sticky="w", row=0, column=4, padx=5)
        self.tin_entry = CTkEntry(master=create_tab, width=145, border_color="#2A8C55", border_width=2)
        self.tin_entry.grid(sticky="w", row=0, column=5, padx=5)

        # Second Row
        CTkLabel(master=create_tab, text="Terms:").grid(sticky="w", row=1, column=0, padx=5)
        self.terms_entry = CTkComboBox(master=create_tab, width=145, values=["CASH", "CHECK"], button_color="#2A8C55",
                                       border_color="#2A8C55", border_width=2)
        self.terms_entry.grid(sticky="w", row=1, column=1, padx=5)

        CTkLabel(master=create_tab, text="Contact Person:").grid(sticky="w", row=1, column=2, padx=5)
        self.contactp_entry = CTkEntry(master=create_tab, width=145, border_color="#2A8C55", border_width=2)
        self.contactp_entry.grid(sticky="w", row=1, column=3, padx=5)

        CTkLabel(master=create_tab, text="Contact No:").grid(sticky="w", row=1, column=4, padx=5)
        self.contactno_entry = CTkEntry(master=create_tab, width=145, border_color="#2A8C55", border_width=2)
        self.contactno_entry.grid(sticky="w", row=1, column=5, padx=5)

        # Add Button
        self.add_supplier_button = CTkButton(master=create_tab, text="Submit", fg_color="green", hover_color="#207244",
                                             font=("Arial Bold", 15), width=145, command=self.add_supplier)
        self.add_supplier_button.grid(sticky="w", row=2, column=5, padx=5, pady=5)

        # Get Treeview from Master
        self.tk_tree = master.tree.treeview
        self.all_rows = master.all_rows

    def search_callback(self, _):
        search_value = self.search.get().strip().lower()  # Normalize input for case-insensitive search

        # Clear existing Treeview data
        self.tk_tree.delete(*self.tk_tree.get_children())

        # Filter rows based on search
        filtered_rows = []
        for item in self.all_rows:
            for key, value in item.items():
                if search_value in str(value[0]).lower():
                    filtered_rows.append(item)

        # Manually Repopulate the tree with filtered data
        for index, item in enumerate(filtered_rows):  # Get index and dictionary
            for key, value in item.items():  # Get key value pair inside dictionary
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tk_tree.insert("", "end", iid=key, values=value, tags=(tag,))

    def add_supplier(self):
        entries = {
            "name": self.name_entry.get(), "address": self.address_entry.get(), "tin_no": self.tin_entry.get(),
            "contactp": self.contactp_entry.get(), "contactno": self.contactno_entry.get(), "terms": self.terms_entry.get()
        }

        if "" == entries.get("name"):
            messagebox.showerror("Error",
                                 "Failed to add entry to the database.\n\nPossible reasons:"
                                 "\n- Missing name entry.\n- There was an unexpected issue."
                                 "\n\nPlease check and try again.")
        else:
            # Add New Supplier to Database
            name, address, tin_no = entries.get("name"), entries.get("address"), entries.get("tin_no")
            contact_p, contact_no, terms = entries.get("contact_p"), entries.get("contact_no"), entries.get("terms")
            iid = str(uuid4())[:6]
            values = [name, address, tin_no, terms]

            supp_ctrl.add_supplier(
                iid=iid,
                name=name,
                address=address,
                tin_no=tin_no,
                contact_p=contact_p,
                contact_no=contact_no,
                terms=terms
            )

            self.tk_tree.insert(parent='', index=0, iid=iid, text='', values=values)
            helper.refresh_stripes(self.tk_tree)
            # Update All Rows
            self.all_rows = helper.return_updated_suppliers()
            self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.tin_entry.delete(0, END)
        self.contactp_entry.delete(0, END)
        self.contactno_entry.delete(0, END)
        self.terms_entry.set("")
