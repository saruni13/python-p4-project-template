#!/usr/bin/env python3
from models import db, Product, Supplier, Transaction, Order, User
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
db.init_app(app)
api = Api(app)

@app.route('/')
def index():
    return '<h1>Phase 4 Final Challenge</h1>'

class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return jsonify(product.to_dict())
            return {'error': 'Product not found'}, 404
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])

    def post(self):
        data = request.get_json()
        try:
            new_product = Product(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                supplier_id=data["supplier_id"],
                date=data["date"]
            )

            db.session.add(new_product)
            db.session.commit()
            return jsonify(new_product.to_dict()), 201
        except Exception as e:
            return {'error': str(e)}, 400

class SupplierResource(Resource):
    def get(self, supplier_id=None):
        if supplier_id:
            supplier = Supplier.query.get(supplier_id)
            if supplier:
                return jsonify(supplier.to_dict())
            return {'error': "Supplier not found!"}, 404
        suppliers = Supplier.query.all()
        return jsonify([supplier.to_dict() for supplier in suppliers])

    def post(self):
        data = request.get_json()
        try:
            new_supplier = Supplier(
                name=data["name"],
                description=data["description"],
                date=data["date"]
            )

            db.session.add(new_supplier)
            db.session.commit()
            return jsonify(new_supplier.to_dict()), 201
        except Exception as e:
            return {'error': str(e)}, 400

class TransactionResource(Resource):
    def get(self, transaction_id=None):
        if transaction_id:
            transaction = Transaction.query.get(transaction_id)
            if transaction:
                return jsonify(transaction.to_dict())
            return {'error': "Transaction not found!"}, 404
        transactions = Transaction.query.all()
        return jsonify([transaction.to_dict() for transaction in transactions])

    def post(self):
        data = request.get_json()
        try:
            new_transaction = Transaction(
                quantity=data["quantity"],
                product_id=data["product_id"],
                date=data["date"]
            )

            db.session.add(new_transaction)
            db.session.commit()
            return jsonify(new_transaction.to_dict()), 201
        except Exception as e:
            return {'error': str(e)}, 400

class OrderResource(Resource):
    def get(self, order_id=None):
        if order_id:
            order = Order.query.get(order_id)
            if order:
                return jsonify(order.to_dict())
            return {'error': "Order not found!"}, 404
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders])

    def post(self):
        data = request.get_json()
        try:
            new_order = Order(
                description=data["description"],
                quantity=data["quantity"],
                price=data["price"],
                product_id=data["product_id"],
                date_received=data["date_received"]
            )

            db.session.add(new_order)
            db.session.commit()
            return jsonify(new_order.to_dict()), 201
        except Exception as e:
            return {'error': str(e)}, 400

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return jsonify(user.to_dict())
            return {'error': "User not found!"}, 404
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    def post(self):
        data = request.get_json()
        try:
            new_user = User(
                name=data["name"],
                email=data["email"],
                role=data["role"]
            )
            new_user.set_password(data["password"])
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201
        except Exception as e:
            return {'error': str(e)}, 400

api.add_resource(ProductResource, '/products', '/products/<int:product_id>')
api.add_resource(SupplierResource, '/suppliers', '/suppliers/<int:supplier_id>')
api.add_resource(TransactionResource, '/transactions', '/transactions/<int:transaction_id>')
api.add_resource(OrderResource, '/orders', '/orders/<int:order_id>')
api.add_resource(UserResource, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
