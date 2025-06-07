from customtkinter import CTkTabview, CTkButton, CTkFrame
import helper
from datetime import datetime


class SalesTabView(CTkTabview):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Configure TabView Style
        self.configure(height=130, segmented_button_fg_color="#99BC85", segmented_button_selected_color="#E4EFE7", segmented_button_selected_hover_color="#E4EFE7", segmented_button_unselected_hover_color="#E4EFE7",
                       segmented_button_unselected_color="#99BC85", text_color="black", text_color_disabled="black", anchor="nw")
        self._segmented_button.configure(font=("Arial Bold", 12), corner_radius=5)

        # Add Tabs
        self.table_tab = self.add("Table")

        # Initialize Table Tab
        t_first_row = CTkFrame(self.table_tab, fg_color="transparent")
        t_first_row.pack(fill="x", expand=True)

        self.search_label, self.search_entry = helper.create_labeled_entry(master=t_first_row, label="Search Customer:", row=0, column=0, width=305)
        self.search_entry.bind("<Return>", self.filter)
        self.search_entry.bind("<KeyRelease>", command=self.check_search)
        self.search_button = CTkButton(master=t_first_row, text="Search", fg_color="green", hover_color="#207244", font=("Arial Bold", 12), width=20, command=lambda: self.filter(None))
        self.search_button.grid(row=0, column=3)

        t_second_row = CTkFrame(self.table_tab, fg_color="transparent")
        t_second_row.pack(fill="x", expand=True)

        year_options = ["All", "2023", "2024", "2025"]
        self.year_label, self.year_filter = helper.create_labeled_entry(master=t_second_row, label="Year:", row=0, column=0, entry_type="combo", values=year_options, command=self.filter)
        month_options = ["All", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.month_label, self.month_filter = helper.create_labeled_entry(master=t_second_row, label="Month:", row=0, column=2, entry_type="combo", values=month_options, command=self.filter)
        status_options = ["All", "Ordered", "Posted", "Paid"]
        self.status_filter_label, self.status_filter = helper.create_labeled_entry(master=t_second_row, label="Status:", row=0, column=4, entry_type="combo", values=status_options, command=self.filter)

        # Get Treeview from Master
        self.tree = master.tree
        self.tk_tree = master.tree.treeview
        self.all_rows = master.all_rows

    def filter(self, _):
        """Function to apply multiple filters to Treeview"""
        # Get All Filters
        year = self.year_filter.get()
        month = self.month_filter.get()
        status = self.status_filter.get()
        search = self.search_entry.get().strip().lower()

        month_dict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                      "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

        # Show all reports if filtering "All"
        if year == "All" and month == "All" and status == "All" and search == "":
            self.tree.show_sales()
            return

        # Refresh Treeview
        self.tk_tree.delete(*self.tk_tree.get_children())
        self.tree.show_sales()

        # Filter
        rows = []
        for item in self.all_rows:
            for key, value in item.items():
                matches_search = (search == "" or search in value[2].lower())
                matches_year = (year == "All" or datetime.strptime(value[0], "%m/%d/%Y").year == int(year))
                matches_month = (month == "All" or value[0].split('/')[0] == month_dict.get(month))
                matches_status = (status == "All" or value[-1] == status)

                if matches_search and matches_year and matches_month and matches_status:
                    rows.append(item)

        # Show Rows
        self.tk_tree.delete(*self.tk_tree.get_children())
        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            for iid, data in row.items():
                self.tk_tree.insert(parent='', index='end', iid=iid, values=data, tags=(tag,))

        # Compute for Total
        if hasattr(self.master, "total_label"):
            helper.compute_tree_total(self.tk_tree, self.master.total_label)

    def check_search(self, _):
        if not self.search_entry.get():
            # Refresh Treeview
            self.tk_tree.delete(*self.tk_tree.get_children())
            self.tree.show_sales()
            # Call Filter
            self.filter(None)
