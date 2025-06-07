""" Controller to handle CRUD Operations from Collection Table"""
from models import db, app, Collection
from datetime import datetime


# ---------- CREATE ----------
def create_collection(iid, date, customer_name, dr_si_no, amount, remarks, bank_type, check_no, check_date, sales_id, customer_id):
    """Create a new collection entry"""
    with app.app_context():
        new_collection = Collection(
            id=iid,
            date=date,
            customer_name=customer_name,
            dr_si_no=dr_si_no,
            amount=amount,
            remarks=remarks,
            bank_type=bank_type,
            check_no=check_no,
            check_date=check_date,
            sales_id=sales_id,
            customer_id=customer_id
        )
        db.session.add(new_collection)
        db.session.commit()


# ---------- READ ----------
def get_all_collections():
    with app.app_context():
        rows = Collection.query.order_by(Collection.date).all()
        row_sorted = sorted(rows, key=lambda x: datetime.strptime(x.date, "%m/%d/%Y"), reverse=True)
        return [{row.id: [row.date, row.customer_name, row.dr_si_no, row.amount]} for row in row_sorted]

# ---------- UPDATE ----------
# ---------- DELETE ----------



