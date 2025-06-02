""" Controller to handle CRUD Operations from Supplier Table"""
from models import db, app, Supplier


# ---------- CREATE ----------
def add_supplier(iid, name, address, tin_no, contact_p, contact_no, terms):
    with app.app_context():
        new_supplier = Supplier(
            id=iid,
            name=name,
            address=address,
            tin_no=tin_no,
            contact_person=contact_p,
            contact_no=contact_no,
            terms=terms
        )
        db.session.add(new_supplier)
        db.session.commit()


# ---------- READ ----------
def get_all_supp():
    with app.app_context():
        return Supplier.query.order_by(Supplier.name).all()


def get_supp_names():
    with app.app_context():
        return [supplier.name for supplier in Supplier.query.order_by(Supplier.name).all()]


# ---------- DELETE ----------
def delete_supp(iid):
    with app.app_context():
        supplier = db.session.query(Supplier).filter(Supplier.id == iid).first()
        db.session.delete(supplier)
        db.session.commit()
