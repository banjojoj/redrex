from models import db, app, Purchases, PurchaseDetails
from datetime import datetime


# ---------- CREATE ----------
def add_purchase(iid, date, dr_si_no, status, total, supplier_id):
    with app.app_context():
        new_purchase = Purchases(
            id=iid,
            date=date,
            dr_si_no=dr_si_no,
            status=status,
            total=total,
            supplier_id=supplier_id,
        )
        db.session.add(new_purchase)
        db.session.commit()


def add_purch_details(iid, quantity, price, sub_total, serial_nos, product_id, purchase_id):
    with app.app_context():
        new_purch_details = PurchaseDetails(
            id=iid,
            quantity=quantity,
            price=price,
            sub_total=sub_total,
            serial_nos=serial_nos,
            product_id=product_id,
            purchase_id=purchase_id
        )
        db.session.add(new_purch_details)
        db.session.commit()


# ---------- UPDATE ----------


# ---------- READ ----------
def get_all_purchases():
    """Return List of Dictionaries"""
    with app.app_context():
        rows = Purchases.query.order_by(Purchases.date).all()
        row_sorted = sorted(rows, key=lambda x: datetime.strptime(x.date, "%m/%d/%Y"), reverse=True)
        return [{row.id: [row.date, row.dr_si_no, row.supplier.name, row.total, row.status]} for row in row_sorted]


# ---------- DELETE ----------
def delete_purch(iid):
    with app.app_context():
        # Find Purchase Details referencing purchase
        purchase = db.session.query(Purchases).filter(Purchases.id == iid).first()
        purchase_details = db.session.query(Purchases).filter(Purchases.purchase_id == Purchases.id).all()

        # Remove all purchase details referencing sale
        for pd in purchase_details:
            db.session.delete(pd)
            db.session.commit()

        db.session.delete(purchase)
        db.session.commit()
