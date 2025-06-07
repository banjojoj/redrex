from models import db, app, Sales, SaleDetails
from datetime import datetime


# ---------- CREATE ----------
def add_sales(iid, date, dr_si_no, status, total, customer_id):
    with app.app_context():
        new_sales = Sales(
            id=iid,
            date=date,
            dr_si_no=dr_si_no,
            status=status,
            total=total,
            customer_id=customer_id
        )
        db.session.add(new_sales)
        db.session.commit()


def add_sales_details(iid, quantity, price, sub_total, serial_nos, product_id, sales_id):
    with app.app_context():
        new_sale_detail = SaleDetails(
            id=iid,
            quantity=quantity,
            price=price,
            sub_total=sub_total,
            serial_nos=serial_nos,
            product_id=product_id,
            sales_id=sales_id,
        )
        db.session.add(new_sale_detail)
        db.session.commit()


# ---------- UPDATE ----------
def update_sales_total(iid, total):
    with app.app_context():
        sale = db.session.query(Sales).filter(Sales.id == iid).first()
        sale.total = total
        db.session.commit()


def update_sales_status(dr_si_no, status):
    """Update Sales Status"""
    with app.app_context():
        sale = db.session.query(Sales).filter(Sales.dr_si_no == dr_si_no).first()
        sale.status = status
        db.session.commit()


# ---------- READ ----------
def get_all_sales():
    """Return List of Dictionaries"""
    with app.app_context():
        rows = Sales.query.order_by(Sales.date).all()
        row_sorted = sorted(rows, key=lambda x: datetime.strptime(x.date, "%m/%d/%Y"), reverse=True)
        return [{row.id: [row.date, row.dr_si_no, row.customer.name, row.total, row.status]} for row in row_sorted]


def get_sales_rows():
    """Returns Rows to display for Sales Treeview"""
    with app.app_context():
        response = Sales.query.order_by(Sales.date).all()
        rows = [(s.id, s.date, s.dr_si_no, s.customer.name, s.total, s.status) for s in response]
        row_sorted = sorted(rows, key=lambda x: datetime.strptime(x[1], "%m/%d/%Y"), reverse=True)
        return row_sorted


def get_sales_id(dr_si_no, date=None):
    with app.app_context():
        if not date:
            sales = db.session.query(Sales).filter(Sales.dr_si_no == dr_si_no).first()
            return sales.id
        sales = db.session.query(Sales).filter(Sales.dr_si_no == dr_si_no, Sales.date == date).first()
        return sales.id


def get_drsi_values():
    """Returns List of DR/SI Values"""
    with app.app_context():
        sales = db.session.query(Sales).all()
        drsi_values = [sale.dr_si_no for sale in sales if sale.status != "Paid"]
        return drsi_values


def get_sales_details(dr_si_no):
    """Returns Details in a Sales Record"""
    with app.app_context():
        sales = db.session.query(Sales).filter_by(dr_si_no=dr_si_no).first()
        sale_details = sales.sale_details

        details = []
        for sd in sale_details:
            sd_dict = {
                "quantity": sd.quantity,
                "price": sd.price,
                "sub_total": sd.sub_total,
                "serial_nos": sd.serial_nos,
                "product": sd.product.description,
            }
            details.append(sd_dict)

        return details


# ---------- DELETE ----------
def delete_sale(iid):
    with app.app_context():
        # Find Sale Details referencing sale
        sale = db.session.query(Sales).filter(Sales.id == iid).first()
        sale_details = db.session.query(SaleDetails).filter(SaleDetails.sales_id == sale.id).all()

        # Remove sale details referencing sale
        for sd in sale_details:
            db.session.delete(sd)
            db.session.commit()

        db.session.delete(sale)
        db.session.commit()
