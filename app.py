from customtkinter import CTkFrame, set_appearance_mode, set_default_color_theme, CTk
from gui.sidebar import Sidebar
from gui import product_view, customer_view, supplier_view, sales_view, purchases_view, collection_view
from gui.create import create_new_sale, create_new_purchase
from models import app, db

# Set Themes for Application
set_appearance_mode("light")
set_default_color_theme("dark-blue")

# Create Variables app and db for migrations
app = app
db = db


# Create Screen
class App(CTk):
    def __init__(self):
        super().__init__()
        # Initialize Application
        self.title("Rex | RedCircuit")
        self.after(0, lambda: self.state("zoomed"))

        # Create Sidebar
        self.sidebar = Sidebar(master=self)
        self.sidebar.pack_propagate(False)
        self.sidebar.pack(side="left", fill="y")

        # Create Container for Views and Initialize Views
        view_container = CTkFrame(master=self, fg_color="transparent")
        view_container.pack(side="right", fill="both", expand=True)
        view_container.grid_rowconfigure(0, weight=1)
        view_container.grid_columnconfigure(0, weight=1)

        s_view = sales_view.SalesView(view_container, show_view=self.show_view)
        p_view = purchases_view.PurchasesView(view_container, show_view=self.show_view)
        self.views = {
            "ProductView": product_view.ProductView(view_container),
            "CustomerView": customer_view.CustomerView(view_container),
            "SupplierView": supplier_view.SupplierView(view_container),
            "SalesView": s_view,
            "CreateNewSale": create_new_sale.CreateNewSale(view_container, show_view=self.show_view, s_view=s_view),
            "PurchasesView": p_view,
            "CreateNewPurchase": create_new_purchase.CreateNewPurchase(view_container, show_view=self.show_view, p_view=p_view),
            "CollectionView": collection_view.CollectionView(view_container)
        }

        # Show all views initially
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

        self.current_view = None
        self.show_view("ProductView")

    def show_view(self, view):
        self.current_view = self.views[view]
        self.current_view.lift()


main_app = App()
main_app.mainloop()
