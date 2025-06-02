""" Controller to handle CRUD Operations from Collection Table"""
from models import db, app, Collection
from datetime import datetime


# ---------- CREATE ----------
# ---------- READ ----------
def get_all_collections():
    with app.app_context():
        rows = Collection.query.order_by(Collection.date).all()
        row_sorted = sorted(rows, key=lambda x: datetime.strptime(x.date, "%m/%d/%Y"), reverse=True)
        return [{row.id: [row.date, row.customer_name, row.dr_si_no, row.amount]} for row in row_sorted]

# ---------- UPDATE ----------
# ---------- DELETE ----------



