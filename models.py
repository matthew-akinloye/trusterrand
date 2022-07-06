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


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), default=0)
    description = db.Column(db.Text)
    category = db.Column(db.String(12))
    pictures = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return "<Product {}>".format(self.title)


class Addresses(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, index=True)
    address = db.Column(db.String(200))
    street = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(5))

    def __repr__(self):
        return "<Address {}>".format(self.address)
