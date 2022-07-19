
from datetime import timedelta
from unicodedata import category

from flask import render_template, request, flash, session, redirect, url_for
import hashlib

from sqlalchemy import null

from index import db, app
from models import User, Products,Category
from user_functions import check_user


@app.route('/')
def homepage():
    user_profile = check_user()
    products = Products.query.all()
    categories = Category.query.all()
    # convert all product image strings to list
    for product in products:
        product.images = product.images.split(',')    
    return render_template('index.html', user_profile=user_profile, products=products, categories=categories)


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')





@app.route('/shop')
def shop():
    user_profile = check_user()
    products = Products.query.all()
    categories = Category.query.all()
    # convert all product image strings to list
    for product in products:
        product.images = product.images.split(',')    
    return render_template('shop.html', user_profile=user_profile, products=products, categories=categories)

@app.route('/dashboard')
def dashboard():
    user_profile = check_user()
    products = Products.query.all()
    categories = Category.query.all()
    # convert all product image strings to list
    for product in products:
        product.images = product.images.split(',')    
    return render_template('admin.html', user_profile=user_profile, products=products, categories=categories)
    
@app.route('/logout')
def logout():
    # removing sessions
    session.pop('email')
    session.pop('password')
    session.pop('id')                                                           
    # removing cookies
    resp = redirect(url_for('homepage'))
    resp.set_cookie('user_id', max_age=0)
    resp.set_cookie('pw', max_age=0)
    return resp


@app.route('/do-login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    correct_user = User.query.filter_by(email=email).first()
    if correct_user is not None:
        if correct_user.password_hash == password_hash:
            flash("Welcome " + correct_user.firstname)
            # save session 
            session['email'] = email
            session['password'] = password
            session['id'] = correct_user.id
            
            response = redirect(url_for('dashboard'))
            response.set_cookie('user_id', str(correct_user.id),
                                max_age=timedelta(hours=24))
            response.set_cookie('pw', password_hash,
                                max_age=timedelta(hours=24))
            return response

    flash("Invalid email or password")
   
    return redirect(url_for('login_page'))



@app.route('/product/<pid>')
def view_product(pid):
    pid = int(pid)
    ans = pid * 4
    return "You are looking for product {}".format(ans)


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/do-sign-up', methods=['POST'])
def do_signup():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']
    
    if firstname == '' or lastname == '' or email == '' or password == '' or password2 == '':
        flash('All fields are required!')
        return redirect(url_for('register_page'))
    if password != password2:
        flash('Passwords does not match')
        return redirect(url_for('register_page'))
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    user_exist = User.query.filter_by(email=email).first()
    if user_exist is not None:
        flash('Ooops, email already exist ')
        return redirect(url_for('register_page'))

    new_user = User(firstname=firstname, lastname=lastname, email=email,
                    password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    # save session
    session['email'] = email
    session['password'] = password
    session['id'] = new_user.id
    response = redirect(url_for('dashboard'))
    response.set_cookie('user_id', str(new_user.id),
                        max_age=timedelta(hours=24))
    response.set_cookie('pw', password_hash,
                        max_age=timedelta(hours=24))
    return response


