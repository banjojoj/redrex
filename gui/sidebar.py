from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkOptionMenu, CTkButton
from PIL import Image

# Constants for Elements in the Sidebar
BUTTON_WIDTH = 150
FONT = ("Arial Bold", 11)
FG_COLOR = "#fff"
HOVER_COLOR = "#eee"
TEXT_COLOR = "#2A8C55"


class Sidebar(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.configure(width=250)
        self.master = master

        # Logo
        logo_img_data = Image.open("assets/logo.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(150, 150))
        self.sidebar_logo = CTkLabel(master=self, text="", image=logo_img).pack(pady=30, anchor="center")
        self.insert_divider()

        # -------- Create Sidebar Elements --------
        # Define Button Attributes
        self.button_config = {
            "fg_color": FG_COLOR,
            "font": FONT,
            "text_color": TEXT_COLOR,
            "hover_color": HOVER_COLOR,
            "width": BUTTON_WIDTH,
            "anchor": "w"
        }

        # Create Sidebar Buttons
        self.product_button = self.create_button(self, text="Products", command=lambda: master.show_view("ProductView"))

        self.people_menu = CTkOptionMenu(self, values=["Customers", "Suppliers"], fg_color=FG_COLOR, font=FONT, text_color=TEXT_COLOR, width=BUTTON_WIDTH, height=35, anchor="w",
                                         dropdown_fg_color=FG_COLOR, button_color="light green", button_hover_color="white", dropdown_text_color=TEXT_COLOR,
                                         command=lambda choice: self.people_menu_callback(choice, master))
        self.people_menu.pack(pady=5)

        # More Buttons
        self.transaction_menu = CTkOptionMenu(self, values=["Sales", "Purchases"], fg_color=FG_COLOR, font=FONT, text_color=TEXT_COLOR, width=BUTTON_WIDTH, height=35, anchor="w",
                                              dropdown_fg_color=FG_COLOR, button_color="light green", button_hover_color="white", dropdown_text_color=TEXT_COLOR,
                                              command=lambda choice: self.transaction_menu_callback(choice, master))
        self.transaction_menu.pack(pady=5)
        # self.create_button(self, "Sales Order", "sampleApp/package_icon.png", None)
        # self.create_button(self, "Purchase Order", "sampleApp/package_icon.png", None)
        self.create_button(self, "Collection", command=lambda: master.show_view("CollectionView"))
        # self.create_button(self, "Report", "sampleApp/package_icon.png", None)

    def create_button(self, master, text, command=None):
        """Creates a sidebar button and returns the button instance."""
        button = CTkButton(master=master, text=text, command=command, **self.button_config)
        button.pack(anchor="center", ipady=5, pady=5)
        return button  # Return button instance

    def people_menu_callback(self, choice, master):
        """Callback Function when Selection from People Option Menu"""
        if choice == "Customers":
            master.show_view("CustomerView")
        else:
            master.show_view("SupplierView")

    def transaction_menu_callback(self, choice, master):
        """Callback Function when Selection from Transaction Option Menu"""
        if choice == "Sales":
            master.show_view("SalesView")
        else:
            master.show_view("PurchasesView")

    def insert_divider(self):
        # Create Divider inside Sidebar
        sidebar_divider = CTkFrame(self, height=2, fg_color="black")
        sidebar_divider.pack(fill="x", padx=15, pady=10)
