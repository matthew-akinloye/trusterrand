
from flask import render_template, redirect, url_for, flash

from errands import pics_to_array
from index import app
from models import Products, Category


# Search Products
@app.route('/search/<term>')
def search_product(term):
    products = Products.query.filter.filter(
        Products.category.ilike('%' + term + '%')
        | Products.handle.ilike('%' + term + '%')
        | Products.title.ilike('%' + term + '%')
    ).filter(Products.status == 'active').all()
    map(pics_to_array, products)
    return render_template('shop.html', products=products, search_term=term)


# Get details of a single product by it's handle
@app.route('/products/<handle>')
def get_product(handle):
    product = Products.query.filter_by(handle=handle).first()
    if product is None:
        flash("Product not found!")
        return redirect(url_for('homepage'))

    product.images = product.images.split(',')
    return render_template('detail.html', product=product)


# get products by category
@app.route('/categories/<cat>')
def get_category_products(cat):
    category = Category.query.filter(Category.handle == cat).first()
    if category is None:
        flash("Category not found!")
        return redirect(url_for('homepage'))
    products = Products.query.filter(Products.category == cat).all()
    map(pics_to_array, products)
    return render_template('shop.html', products=products, category=category)
