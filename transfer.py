from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from oldApp.database import CollectionTable
from flask import Flask
import os
from datetime import datetime
from uuid import uuid4
import ast
import models
from fuzzywuzzy import process


# Get the AppData folder and Create Path for Database
db_folder = os.path.join(os.getenv("APPDATA"), "RedRex")
os.makedirs(db_folder, exist_ok=True)  # Ensure the folder exists
db_path = os.path.join(db_folder, "redrex.db")


# Initialize App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///C:/Users/dell/PycharmProjects/RexRed/oldApp/inventory.db'


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)    # Initialize app

with models.app.app_context():
    all_collections = models.db.session.query(models.Collection).all()
    total = len(all_collections)

with app.app_context():
    result = db.session.execute(db.select(CollectionTable))
    collection = result.scalars().all()
    index = 0

    for item in collection:
        collection_dict = {
            "id": item.id,
            "date": item.date,
            "customer": item.customer,
            "amount": float(item.amount),
            "remarks": item.remarks,
            "bank_type": item.bank_type,
            "check_no": item.check_no,
            "check_date": item.check_date,
            "dr_si_no": ast.literal_eval(item.dr_si_no),
        }

        # Find Customer
        for dr_si in collection_dict.get("dr_si_no"):
            with models.app.app_context():
                customer = models.db.session.query(models.Customer).filter_by(name=item.customer).first()

                for coll in all_collections:
                    if coll.dr_si_no == dr_si:
                        if customer:
                            coll.customer_name = customer.name
                            coll.customer_id = customer.id
                        else:
                            print(item.customer)
                            coll.customer_name = item.customer

                        # models.db.session.commit()
                        index += 1
                        print(f"{index}/{total}")
