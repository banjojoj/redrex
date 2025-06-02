""" Controller to handle CRUD Operations from Product Table"""
from models import db, app, Product


# ---------- CREATE ----------
def add_product(iid, description, p_type, cost, price, stock):
    with app.app_context():
        new_product = Product(
            id=iid,
            description=description,
            type=p_type,
            cost=cost,
            price=price,
            stock=stock,
        )
        db.session.add(new_product)
        db.session.commit()


# ---------- READ ----------
def get_prodby_desc():
    with app.app_context():
        return Product.query.order_by(Product.description).all()


def get_prodby_type():
    with app.app_context():
        return Product.query.order_by(Product.type).all()


def get_prod_types():
    with app.app_context():
        result = [item[0] for item in db.session.query(Product.type).all()]
        types = []
        # Only add types that are commonly used
        for item in result:
            count = result.count(item)
            if count > 10:
                types.append(item)

        return list(set(types))[0:10]


def get_prod_descs():
    with app.app_context():
        return [product.description for product in Product.query.order_by(Product.description).all()]


def get_prod_id(product_desc):
    with app.app_context():
        product = db.session.query(Product).filter(Product.description == product_desc).first()
        return product.id


# ---------- DELETE ----------
def delete_prod(iid):
    with app.app_context():
        product = db.session.query(Product).filter(Product.id == iid).first()
        db.session.delete(product)
        db.session.commit()











