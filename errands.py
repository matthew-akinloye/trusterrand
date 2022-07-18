import string

from faker import Faker
import random

from flask import request
from slugify import slugify

from index import db
from models import Category, Products

fake = Faker()


def delete_categories(amount: int):
    if amount == 0:
        Category.query().delete()
        print('All categories deleted..')
    else:
        Category.query().limit(amount).delete()
        print('deleted {} categories'.format(amount))


def delete_products(amount: int):
    if amount == 0:
        Products.query().delete()
        print('All categories deleted..')
    else:
        Products.query().limit(amount).delete()
        print('deleted {} categories'.format(amount))


def create_dummy_products(amount):
    i = 0
    while amount > i:
        title = fake.name()
        old_price = random.randint(200, 10000)
        price = old_price - random.randint(100, old_price)
        description = fake.text()
        categories = ['Cloths', 'Shoes', 'Belts']
        cat = random.choice(categories)
        pics = ["https://picsum.photos/seed/{}/200/200".format(cat),
                "https://picsum.photos/seed/{}/200/200".format(cat + '2')]

        handle = slugify(title)
        while bool(Products.query.filter_by(handle=handle).first()):
            handle = slugify(title + ' ' + id_generator(3))

        new_product = Products(title=title, old_price=old_price, price=price, handle=handle,
                               description=description, category=cat,
                               images=','.join(pics), quantity=2, weight=2)
        db.session.add(new_product)
        db.session.commit()
        i += 1
    print("Generated {} dummy products!".format(i))


def create_dummy_category(amount):
    i = 0
    while amount > i:
        title = fake.name()
        description = fake.text()
        amount = fake.random.randint(2, 10000)

        handle = slugify(title)
        while bool(Category.query.filter_by(handle=handle).first()):
            handle = slugify(title + ' ' + id_generator(3))

        new_category = Category(title=title, handle=handle,
                                description=description, amount=amount)
        db.session.add(new_category)
        db.session.commit()
        i += 1
    print("Generated {} dummy categories!".format(i))


def generate_sku():
    return "".join([random.choice(string.digits) for i in range(3)]) + "-" + "".join(
        [random.choice(string.ascii_uppercase) for i in range(3)]) + "-" + "".join(
        [random.choice(string.digits) for i in range(3)])


def get_ip():
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    return ip


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def group_int(number):
    number = int(number)
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))
