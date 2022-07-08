from faker import Faker
import random

from index import db
from models import Products

fake = Faker()


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

        new_product = Products(title=title, old_price=old_price, price=price,
                               description=description, category=cat,
                               pictures=''.join(pics))
        db.session.add(new_product)
        db.session.commit()
        i += 1
    print("Generated {} dummy products!".format(i))
