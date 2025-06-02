from customtkinter import CTkTabview, CTkEntry, CTkLabel, CTkComboBox, CTkButton, END
from controller import prod_ctrl
from tkinter import messagebox
from uuid import uuid4
import helper


class ProductTabView(CTkTabview):
    
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
        self.search = CTkEntry(master=table_tab, width=305, placeholder_text="Search Products...", border_color="#99BC85", border_width=2)
        self.search.bind("<KeyRelease>", self.search_callback)
        self.search.pack(side="left", padx=(13, 0), pady=15)

        CTkLabel(master=table_tab, text="Sort by:").pack(side="left", padx=(10, 0), pady=15)
        sort_options = ["Description", "Type"]
        self.sort_filter = CTkComboBox(master=table_tab, width=125, values=sort_options, button_color="#99BC85", border_color="white", border_width=2,
                                       button_hover_color="#E4EFE7", dropdown_hover_color="#E4EFE7", command=lambda choice: master.tree.show_products(choice))
        self.sort_filter.pack(side="left", padx=10, pady=15)

        # Initialize Create Tab
        CTkLabel(master=create_tab, text="Description:").grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))
        self.description_entry = CTkEntry(master=create_tab, width=305, border_color="#2A8C55", border_width=2)
        self.description_entry.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 5))

        CTkLabel(master=create_tab, text="Type:").grid(row=0, column=1, sticky="w", padx=15, pady=(10, 0))
        type_options = prod_ctrl.get_prod_types()
        self.type_combo = CTkComboBox(master=create_tab, width=150, values=type_options, button_color="#2A8C55",
                                      border_color="#2A8C55", border_width=2)
        self.type_combo.grid(row=1, column=1, sticky="w", padx=15, pady=(0, 5))

        CTkLabel(master=create_tab, text="Cost:").grid(row=0, column=3, sticky="w", padx=15, pady=(10, 0))
        self.cost_entry = CTkEntry(master=create_tab, width=100, border_color="#2A8C55", border_width=2)
        self.cost_entry.grid(row=1, column=3, sticky="w", padx=15, pady=(0, 5))

        CTkLabel(master=create_tab, text="Price:").grid(row=0, column=4, sticky="w", padx=15, pady=(10, 0))
        self.price_entry = CTkEntry(master=create_tab, width=100, border_color="#2A8C55", border_width=2)
        self.price_entry.grid(row=1, column=4, sticky="w", padx=15, pady=(0, 5))

        CTkLabel(master=create_tab, text="Stock:").grid(row=0, column=5, sticky="w", padx=15, pady=(10, 0))
        self.stock_entry = CTkEntry(master=create_tab, width=100, border_color="#2A8C55", border_width=2)
        self.stock_entry.grid(row=1, column=5, sticky="w", padx=15, pady=(0, 5))

        # Add Button
        self.add_product_button = CTkButton(master=create_tab, text="Submit", fg_color="green", hover_color="#207244",
                                            font=("Arial Bold", 15), command=self.add_product)
        self.add_product_button.grid(row=1, column=6, sticky="w", padx=15, pady=(0, 5))

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
        for index, item in enumerate(filtered_rows):            # Get index and dictionary
            for key, value in item.items():                     # Get key value pair inside dictionary
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tk_tree.insert("", "end", iid=key, values=value, tags=(tag,))

    def add_product(self):
        # Get Entry Values
        entries = {
            "desc": self.description_entry.get(), "type": self.type_combo.get(), "cost": self.cost_entry.get(),
            "price": self.price_entry.get(), "stock": self.stock_entry.get()
        }

        # Function to check if an entry submitted is a float
        def is_float(a):
            try:
                float(a)
                return True
            except ValueError:
                return False

        # Check Entries
        if "" in entries or not is_float(entries.get("cost")) or not is_float(entries.get("price")) or not is_float(entries.get("stock")):
            messagebox.showerror("Error",
                                 "Failed to add entry to the database.\n\nPossible reasons:"
                                 "\n- Missing Values.\n- Cost, Price, and Stock must be a number.\n- There was an unexpected issue."
                                 "\n\nPlease check and try again.")
        else:
            # Add New Product to Database
            desc, p_type, cost, price, stock = entries.get("desc"), entries.get("type"), float(entries.get("cost")), float(entries.get("price")), int(float(entries.get("stock")))
            iid = str(uuid4())[:6]
            values = [desc, p_type, cost, price, stock]

            prod_ctrl.add_product(
                iid=iid,
                description=desc,
                p_type=p_type,
                cost=cost,
                price=price,
                stock=stock
            )

            self.tk_tree.insert(parent='', index=0, iid=iid, text='', values=values)
            helper.refresh_stripes(self.tk_tree)
            # Update All Rows
            self.all_rows = helper.return_updated_products()
            self.clear_entries()

    def clear_entries(self):
        self.description_entry.delete(0, END)
        self.type_combo.set("")
        self.cost_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.stock_entry.delete(0, END)

    def return_entries(self):
        return [self.description_entry, self.type_combo, self.cost_entry, self.price_entry, self.stock_entry]

