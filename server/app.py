
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from models import db, Product, Transaction, User
from flask_bcrypt import Bcrypt

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

CORS(app)  # Allow requests from all origins

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(email=data["email"], password=data["password"], company_name=data.get("company_name"), country=data.get("country"), city=data.get("city"))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    product = Product(name=data["name"], sku=data["sku"], description=data.get("description"), quantity=data["quantity"], price=data["price"], supplier_id=data["supplier_id"])
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@app.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([transaction.to_dict() for transaction in transactions])

@app.route("/transactions/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        return jsonify(transaction.to_dict())
    return jsonify({"error": "Transaction not found"}), 404

@app.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json()
    user = User.query.get(data["user_id"])
    product = Product.query.get(data["product_id"])
    if user and product:
        transaction = Transaction(user_id=user.id, product_id=product.id, quantity=data["quantity"], total_price=data["total_price"], type=data["type"])
        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.to_dict()), 201
    return jsonify({"error": "User or product not found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)