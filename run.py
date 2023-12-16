from flask_login import LoginManager
from settings import app, db, socketio
from flask import jsonify, request, g
from flask_login import LoginManager, login_user, logout_user, current_user
from models import *
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, create_access_token
from functools import wraps
import datetime

def jwt_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            print(f"Error verifying JWT: {e}")
            return jsonify({"msg": "Invalid or missing JWT"}), 401
        g.user = User.query.filter_by(email=get_jwt_identity()).first()
        if not g.user:
            resp = jsonify({"msg": "User does not exist"}), 401
            return resp
        token = request.headers.get("Authorization")
        # if g.user.token != token and g.user.old_token != token:
        #     resp = jsonify({"msg": "Bad token"}), 401
        #     return resp
        return func(*args, **kwargs)

    return decorated

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from flask_login import LoginManager

login_manager = LoginManager(app)
login_manager.login_view = 'login'

MGoClient = MongoClient('mongodb://localhost:27017')

database = MGoClient["warehouse"]
collection = database["warehouse_storage"]

@app.route('/products', methods=['POST'])
@jwt_required
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_data = {'id': product.id, 'name': product.name, 'price': product.price}
    return jsonify(product_data)

@app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

@app.route('/process_order', methods=['POST'])
def process_order():
    data = request.get_json()
    product_id = data.get('product_id')

    product = Product.query.get(product_id)

    if product:
        warehouse_product = database['warehouse_storage'].find_one({'identifyNumber': product.identifynumber})
        if warehouse_product and warehouse_product['storage_count'] > 0:
            collection.update_one({'identifyNumber': product.identifynumber}, {'$inc': {'storage_count': -1}})

            return jsonify({'message': 'Order processed successfully'})

        return jsonify({'error': 'Product not available in the warehouse'}), 400

    return jsonify({'error': 'Product not found'}), 404

@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    response = google.get('/plus/v1/people/me')
    assert response.ok, response.text
    google_user_info = response.json()

    # Replace this with your actual logic to load or create a user
    user = users_db.get('1')  # Assuming there's an admin user with ID '1'

    login_user(user)
    return redirect(url_for('protected'))

@app.route('/orders', methods=['POST'])
@jwt_required
def create_order():
    data = request.get_json()
    product_ids = data['product_ids']
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    new_order = Order(products=products)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'})

@app.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    product_ids = data['product_ids']
    order.products = Product.query.filter(Product.id.in_(product_ids)).all()
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})

@app.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
    return jsonify(product_list)

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    order_list = [{'id': order.id, 'products': [product.id for product in order.products]} for order in orders]
    return jsonify(order_list)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/products/<int:product_id>/similar', methods=['GET'])
def get_similar_products(product_id):
    product = Product.query.get_or_404(product_id)
    similar_products = product.similar_products
    similar_products_data = [{'id': p.id, 'name': p.name, 'price': p.price} for p in similar_products]
    return jsonify(similar_products_data)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    new_user = User(username=username, email=email, password = generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=user.email, expires_delta=datetime.timedelta(days=7))

    return jsonify({'token': token}), 200, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        token = create_access_token(identity=user.email, expires_delta=datetime.timedelta(days=7))
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/user', methods=['GET'])
@jwt_required
def get_user():
    return jsonify({'username': current_user.username, 'email': current_user.email})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    socketio.run(app, port=5000)
