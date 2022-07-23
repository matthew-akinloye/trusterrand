from datetime import datetime

from index import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(15))
    password_hash = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<User {}>".format(self.firstname)


class Addresses(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, index=True)
    address = db.Column(db.String(200))
    street = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(5))

    def __repr__(self):
        return "<Address {}>".format(self.address)


class Variants(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(50))
    value = db.Column(db.String(150))
    price = db.Column(db.NUMERIC(10, 2), nullable=False)
    compareAtPrice = db.Column(db.NUMERIC(10, 2), default=0)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    price = db.Column(db.NUMERIC(10, 2), nullable=False)
    old_price = db.Column(db.NUMERIC(10, 2), default=0)
    handle = db.Column(db.String(70), unique=True, index=True)
    title = db.Column(db.String(220))
    images = db.Column(db.Text)
    category = db.Column(db.String(70))
    description = db.Column(db.Text)
    descriptionHtml = db.Column(db.Text)
    vendor = db.Column(db.String(70))
    productType = db.Column(db.String(70))
    tags = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    weight = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(70), unique=True)

    updatedAt = db.Column(db.DateTime)

    created = db.Column(db.DateTime, default=datetime.now())
    views = db.Column(db.Integer, default=0)

    status = db.Column(db.String(10), default='active')
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220))
    handle = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(220))
    amount = db.Column(db.Integer, default=0)
    image = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<Category: {}, Active: {}>".format(self.title, self.active)

    def hide(self):
        self.active = False
        db.session.commit()
        return self.handle + 'hidden'

    def show(self):
        self.active = True
        db.session.commit()
        return self.handle + 'is visible'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=1)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
