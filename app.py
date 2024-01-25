from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
import random
import sqlite3
from essential_generators import DocumentGenerator

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:123@localhost:3306/ss1314_python")
connection = engine.connect()

# Initialize the DocumentGenerator
gen = DocumentGenerator()

# conn = sqlite3.connect('database.db')
# print("Opened database successfully")
#
# conn.execute('CREATE TABLE students (id ,name TEXT, gender TEXT, age TEXT, address TEXT)')
# conn.close

BASE_URL = 'http://127.0.0.1:5000'

app.config['SECRET_KEY'] = 'your_secret_key_here'

import routes

@app.route('/')
def hello_world():  # put application's code here
    products = []
    categories = []
    for item in range(10):
        products.append(
            {
                'id': 1,
                'name': gen.name(),
                'descript': gen.sentence(),
                'price': random.randint(10, 100)
            },
        )

    for category in range(10):
        categories.append(
            {
                'id': 1,
                'name': 'coca cola',
            },
        )

    return render_template('index.html', products=products, categories=categories)


@app.route('/detail/<string:id>')
def detail(id):
    return render_template('product_detail.html', id=id)


@app.route('/admin')
def admin():
    return render_template('admin/master.html')


@app.route('/admin/user')
def indexUser():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from user")
    rows = cur.fetchall()

    return render_template(
        'admin/user/index.html',
        module='user',
        rows=rows
    )


@app.route('/admin/add_user', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        status = request.form['status']
        if not name or not image or not status:
            flash('All fields are required', 'error')
        else:
            conn = sqlite3.connect("database.db")
            conn.execute("INSERT INTO user (name, image, status) VALUES (?, ?, ?)",
                         (name, image, status))
            conn.commit()
            conn.close()
            flash('Student added successfully', 'success')
            return redirect(url_for('indexUser'))

    return render_template('admin/user/add.html')


@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
def delete_User(id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM user WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('indexUser'))


@app.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
def editUser(id):
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM user WHERE id='{id}'")
    row = cur.fetchall()

    # Check if a product with the given ID was found
    if row:
        # Access the first row (since it's a list of rows)
        user = row[0]

        if request.method == 'POST':
            # Handle the form submission for updating the product's data
            new_name = request.form['name']
            new_image = request.form['image']
            new_status = request.form['status']

            # Perform the update in the database
            cur.execute("UPDATE user SET name=?, image=?, status=? WHERE id=?",
                        (new_name, new_image, new_status, id))
            con.commit()

            # Redirect back to the product list or any other desired page
            return redirect(url_for('indexUser'))

        return render_template('admin/user/edit.html', user=user)  # Pass 'product' to the template
    else:
        # Handle the case where the product with the given ID was not found
        flash('Product not found', 'error')
        return redirect(url_for('indexUser'))


@app.route('/admin/product')
def indexProduct():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from product")
    rows = cur.fetchall()

    return render_template(
        'admin/product/index.html',
        module='product',
        rows=rows
    )


@app.route('/admin/add_product', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'POST':
        name = request.form['name']
        cost = request.form['cost']
        price = request.form['price']
        category = request.form['category']
        image = request.form['image']
        status = request.form['status']
        if not name or not cost or not price or not category or not status or not image:
            flash('All fields are required', 'error')
        else:
            conn = sqlite3.connect("database.db")
            conn.execute(
                "INSERT INTO product (category_id, name, image,  cost, price, status) VALUES (?, ?, ?, ?, ?,?)",
                (category, name, image, cost, price, status))
            conn.commit()
            conn.close()
            flash('Student added successfully', 'success')
            return redirect(url_for('indexProduct'))

    return render_template('admin/product/add.html')


@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_Product(id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM product WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('indexProduct'))


@app.route('/admin/edit_product/<int:id>', methods=['GET', 'POST'])
def editProduct(id):
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM product WHERE id='{id}'")
    row = cur.fetchall()

    # Check if a product with the given ID was found
    if row:
        # Access the first row (since it's a list of rows)
        product = row[0]

        if request.method == 'POST':
            # Handle the form submission for updating the product's data
            new_name = request.form['name']
            new_cost = request.form['cost']
            new_price = request.form['price']
            new_category = request.form['category']
            new_status = request.form['status']
            new_image = request.form['image']

            # Perform the update in the database
            cur.execute("UPDATE product SET name=?, image=?,  cost=?, price=?, category_id=?, status=? WHERE id=?",
                        (new_name, new_image, new_cost, new_price, new_category, new_status, id))
            con.commit()

            # Redirect back to the product list or any other desired page
            return redirect(url_for('indexProduct'))

        return render_template('admin/product/edit.html', product=product)  # Pass 'product' to the template
    else:
        # Handle the case where the product with the given ID was not found
        flash('Product not found', 'error')
        return redirect(url_for('indexProduct'))


# @app.route('/admin/customer')
# def indexCustomer():
#     con = sqlite3.connect("database.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute("select * from customer")
#     rows = cur.fetchall()
#
#     return render_template(
#         'admin/customer/index.html',
#         module='customer',
#         rows=rows
#     )
#
#
# @app.route('/admin/add_customer', methods=['GET', 'POST'])
# def addCustomer():
#     if request.method == 'POST':
#         name = request.form['name']
#         image = request.form['image']
#         status = request.form['status']
#         if not name or not image or not status:
#             flash('All fields are required', 'error')
#         else:
#             conn = sqlite3.connect("database.db")
#             conn.execute("INSERT INTO customer (name, image, status) VALUES (?, ?, ?)",
#                          (name, image, status))
#             conn.commit()
#             conn.close()
#             flash('Student added successfully', 'success')
#             return redirect(url_for('indexCustomer'))
#
#     return render_template('admin/customer/add.html')
#
#
# @app.route('/delete_customer/<int:id>', methods=['GET', 'POST'])
# def delete_Customer(id):
#     conn = sqlite3.connect("database.db")
#     conn.execute("DELETE FROM customer WHERE id=?", (id,))
#     conn.commit()
#     conn.close()
#     flash('Product deleted successfully', 'success')
#     return redirect(url_for('indexCustomer'))
#
#
# @app.route('/admin/edit_customer/<int:id>', methods=['GET', 'POST'])
# def editCustomer(id):
#     con = sqlite3.connect("database.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute(f"SELECT * FROM customer WHERE id='{id}'")
#     row = cur.fetchall()
#
#     # Check if a product with the given ID was found
#     if row:
#         # Access the first row (since it's a list of rows)
#         customer = row[0]
#
#         if request.method == 'POST':
#             # Handle the form submission for updating the product's data
#             new_name = request.form['name']
#             new_image = request.form['image']
#             new_status = request.form['status']
#
#             # Perform the update in the database
#             cur.execute("UPDATE customer SET name=?, image=?, status=? WHERE id=?",
#                         (new_name, new_image, new_status, id))
#             con.commit()
#
#             # Redirect back to the product list or any other desired page
#             return redirect(url_for('indexCustomer'))
#
#         return render_template('admin/customer/edit.html', customer=customer)  # Pass 'product' to the template
#     else:
#         # Handle the case where the product with the given ID was not found
#         flash('Product not found', 'error')
#         return redirect(url_for('indexCustomer'))


# @app.route('/admin/currency')
# def indexCurrency():
#     con = sqlite3.connect("database.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute("select * from currency")
#     rows = cur.fetchall()
#
#     return render_template(
#         'admin/currency/index.html',
#         module='currency',
#         rows=rows
#     )
#
#
# @app.route('/admin/add_currency', methods=['GET', 'POST'])
# def addCurrency():
#     if request.method == 'POST':
#         name = request.form['name']
#         code = request.form['code']
#         symbol = request.form['symbol']
#         is_default = request.form['is_default']
#         sell_out_price = request.form['sell_out_price']
#         if not name or not code or not symbol or not is_default or not sell_out_price:
#             flash('All fields are required', 'error')
#         else:
#             conn = sqlite3.connect("database.db")
#             conn.execute("INSERT INTO currency ( name, code, symbol, is_default, sell_out_price) VALUES (?, ?, ?, ?,?)",
#                          (name, code, symbol, is_default, sell_out_price))
#             conn.commit()
#             conn.close()
#             flash('Student added successfully', 'success')
#             return redirect(url_for('indexCurrency'))
#
#     return render_template('admin/currency/add.html')
#
#
# @app.route('/delete_currency/<int:id>', methods=['GET', 'POST'])
# def delete_Currency(id):
#     conn = sqlite3.connect("database.db")
#     conn.execute("DELETE FROM currency WHERE id=?", (id,))
#     conn.commit()
#     conn.close()
#     flash('Product deleted successfully', 'success')
#     return redirect(url_for('indexCurrency'))
#
#
# @app.route('/admin/edit_currency/<int:id>', methods=['GET', 'POST'])
# def editCurrency(id):
#     con = sqlite3.connect("database.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute(f"SELECT * FROM currency WHERE id='{id}'")
#     row = cur.fetchall()
#
#     # Check if a product with the given ID was found
#     if row:
#         # Access the first row (since it's a list of rows)
#         currency = row[0]
#
#         if request.method == 'POST':
#             # Handle the form submission for updating the product's data
#             new_name = request.form['name']
#             new_code = request.form['code']
#             new_symbol = request.form['symbol']
#             new_is_default = request.form['is_default']
#             new_sell_out_price = request.form['sell_out_price']
#
#             # Perform the update in the database
#             cur.execute("UPDATE currency SET name=?, code=?, symbol=?, is_default=?, sell_out_price=? WHERE id=?",
#                         (new_name, new_code, new_symbol, new_is_default, new_sell_out_price, id))
#             con.commit()
#
#             # Redirect back to the product list or any other desired page
#             return redirect(url_for('indexCurrency'))
#
#         return render_template('admin/currency/edit.html', currency=currency)  # Pass 'product' to the template
#     else:
#         # Handle the case where the product with the given ID was not found
#         flash('Product not found', 'error')
#         return redirect(url_for('indexCurrency'))
#

if __name__ == '__main__':
    app.run()
