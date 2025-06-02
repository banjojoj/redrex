from customtkinter import CTkTabview, CTkEntry, CTkLabel, CTkComboBox, CTkButton, END
from controller import prod_ctrl
from tkinter import messagebox
from uuid import uuid4
import helper


class CollectionTabView(CTkTabview):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Configure TabView Style
        self.configure(height=130, segmented_button_fg_color="#99BC85", segmented_button_selected_color="#E4EFE7",
                       segmented_button_selected_hover_color="#E4EFE7",
                       segmented_button_unselected_hover_color="#E4EFE7",
                       segmented_button_unselected_color="#99BC85", text_color="black", text_color_disabled="black",
                       anchor="nw")
        self._segmented_button.configure(font=("Arial Bold", 12), corner_radius=5)

        # Add Tabs
        table_tab = self.add("Table")
        create_tab = self.add("Create")

        # Initialize Table Tab
        self.search = CTkEntry(master=table_tab, width=305, placeholder_text="Search Customer...",
                               border_color="#99BC85", border_width=2)
        self.search.bind("<KeyRelease>", self.search_callback)
        self.search.pack(side="left", padx=(13, 0), pady=15)

        # Initialize Create Tab
        self.date_label, self.date_entry = helper.create_labeled_entry(master=create_tab, label="Date:", row=0, column=0, width=120)
        self.customer_label, self.customer_entry = helper.create_labeled_entry(master=create_tab, label="Customer:", row=0, column=2, width=305)
        self.amt_label, self.amt_entry = helper.create_labeled_entry(master=create_tab, label="Amount:", row=0, column=4, width=120)
        self.remarks_label, self.remarks_entry = helper.create_labeled_entry(master=create_tab, entry_type="combo", values=["CASH", "CHECK"], label="Remarks:", row=0, column=6, width=120)
        self.bank_label, self.bank_entry = helper.create_labeled_entry(master=create_tab, label="Bank Type:", row=0, column=8, width=120)

        self.check_no_label, self.check_no_entry = helper.create_labeled_entry(master=create_tab, label="Check No:", row=1, column=0, width=120)
        self.check_date_label, self.check_date_entry = helper.create_labeled_entry(master=create_tab, label="Check Date:", row=1, column=2, width=120)
        self.drsi_label, self.drsi_entry = helper.create_labeled_entry(master=create_tab, label="DR/SI No:", row=1, column=4, width=120)

        # Add Button
        self.add_product_button = CTkButton(master=create_tab, text="Submit", fg_color="green", hover_color="#207244", font=("Arial Bold", 15))
        self.add_product_button.grid(row=1, column=9, sticky="w", padx=15, pady=(0, 5))

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
                if search_value in str(value[1]).lower():
                    filtered_rows.append(item)

        # Manually Repopulate the tree with filtered data
        for index, item in enumerate(filtered_rows):  # Get index and dictionary
            for key, value in item.items():  # Get key value pair inside dictionary
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tk_tree.insert("", "end", iid=key, values=value, tags=(tag,))
