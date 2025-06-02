""" Controller to handle CRUD Operations from Customer Table"""
from models import db, app, Customer


# ---------- CREATE ----------
def add_customer(iid, name, address, tin_no, contact_p, contact_no, terms, balance):
    with app.app_context():
        new_customer = Customer(
            id=iid,
            name=name,
            address=address,
            tin_no=tin_no,
            contact_person=contact_p,
            contact_no=contact_no,
            terms=terms,
            balance=balance
        )
        db.session.add(new_customer)
        db.session.commit()


# ---------- READ ----------
def get_all_cust():
    with app.app_context():
        return Customer.query.order_by(Customer.name).all()


def get_cust_names():
    with app.app_context():
        return [customer.name for customer in Customer.query.order_by(Customer.name).all()]


def get_cust_id(customer_name):
    with app.app_context():
        customer = db.session.query(Customer).filter_by(name=customer_name).first()
        return customer.id


# ---------- DELETE ----------
def delete_cust(iid):
    with app.app_context():
        customer = db.session.query(Customer).filter(Customer.id == iid).first()
        db.session.delete(customer)
        db.session.commit()

