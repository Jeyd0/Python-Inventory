from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'Mawi'

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='fds',
            user='root',
            password=''
        )
        if connection.is_connected():
            print('Connected to MySQL database')
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'jade' and password == 'gwapo':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

def product_exists(name):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM products WHERE name = %s", (name,))
            product = cursor.fetchone()
            return product is not None
        except Error as e:
            print(f'Failed to check if product exists: {e}')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection closed')
    return False

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        if product_exists(name):
            error = 'Product already exists!'
        else:
            connection = connect_to_database()
            if connection:
                try:
                    cursor = connection.cursor()
                    sql = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (name, price, quantity))
                    connection.commit()
                    flash('Product added successfully!', 'success')
                    return redirect(url_for('add_product'))
                except Error as e:
                    print(f'Failed to add product: {e}')
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
                        print('MySQL connection closed')
    return render_template('add_product.html', error=error)

@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    if request.method == 'POST':
        new_price = request.form['new_price']
        new_quantity = request.form['new_quantity']
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                if new_price:
                    sql = "UPDATE products SET price=%s WHERE id=%s"
                    cursor.execute(sql, (new_price, product_id))
                if new_quantity:
                    sql = "UPDATE products SET quantity=%s WHERE id=%s"
                    cursor.execute(sql, (new_quantity, product_id))
                connection.commit()
                return redirect(url_for('view_products'))
            except Error as e:
                print(f'Failed to update product: {e}')
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print('MySQL connection closed')
    return render_template('edit_product.html', product_id=product_id)

@app.route('/edit_product/<int:product_id>', methods=['GET'])
def edit_product(product_id):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if product:
                return render_template('edit_product.html', product=product)
            else:
                return "Product not found"
        except Error as e:
            print(f'Failed to fetch product details: {e}')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection closed')
    return "Failed to fetch product details"

@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    connection = connect_to_database()
    products = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, price, quantity FROM products")
            products = cursor.fetchall()
        except Error as e:
            print(f'Failed to fetch products: {e}')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection closed')

    if request.method == 'POST':
        product_id = request.form['product_id']
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "DELETE FROM products WHERE id=%s"
                cursor.execute(sql, (product_id,))
                connection.commit()
                flash('Product deleted successfully!', 'success')
                return jsonify({'success': True})
            except Error as e:
                print(f'Failed to delete product: {e}')
                return jsonify({'success': False, 'error': str(e)})
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print('MySQL connection closed')
    return render_template('delete_product.html', products=products)

@app.route('/view_products')
def view_products():
    try:
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM products")
                products = cursor.fetchall()
                return render_template('view_products.html', products=products)
            except Error as e:
                print(f'Failed to execute query: {e}')
                products = []
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print('MySQL connection closed')
    except Error as e:
        print(f'Failed to connect to database: {e}')
        products = []
    return render_template('view_products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)