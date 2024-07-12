from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
db.init_app(app)

from models import Supplier, Product, Transaction, Order

@app.route('/supplier', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.__repr__() for supplier in suppliers])

@app.route('/supplier/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    return jsonify(supplier.__repr__())

@app.route('/supplier', methods=['POST'])
def create_supplier():
    data = request.get_json()
    new_supplier = Supplier(
        name=data['name'],
        description=data['description'],
        date=datetime.datetime.utcnow()
    )
    db.session.add(new_supplier)
    try:
        db.session.commit()
        return jsonify({'message': 'Supplier created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/supplier/<int:id>', methods=['PUT'])
def update_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    data = request.get_json()
    supplier.name = data['name']
    supplier.description = data['description']
    try:
        db.session.commit()
        return jsonify({'message': 'Supplier updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/supplier/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    db.session.delete(supplier)
    try:
        db.session.commit()
        return jsonify({'message': 'Supplier deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/product', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.__repr__() for product in products])

@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(product.__repr__())

@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        supplier_id=data['supplier_id'],
        date=datetime.datetime.utcnow()
    )
    db.session.add(new_product)
    try:
        db.session.commit()
        return jsonify({'message': 'Product created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    data = request.get_json()
    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    product.supplier_id = data['supplier_id']
    try:
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    try:
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/transaction', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([transaction.__repr__() for transaction in transactions])

@app.route('/transaction/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    return jsonify(transaction.__repr__())

@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        quantity=data['quantity'],
        product_id=data['product_id'],
        created_at=datetime.datetime.utcnow()
    )
    db.session.add(new_transaction)
    try:
        db.session.commit()
        return jsonify({'message': 'Transaction created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/transaction/<int:id>', methods=['PUT'])
def update_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    data = request.get_json()
    transaction.quantity = data['quantity']
    transaction.product_id = data['product_id']
    try:
        db.session.commit()
        return jsonify({'message': 'Transaction updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/transaction/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    db.session.delete(transaction)
    try:
        db.session.commit()
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    
@app.route('/order', methods=['GET'])
def get_transactions():
    order = Order.query.all()
    return jsonify([order.__repr__() for order in order])

@app.route('/order/<int:id>', methods=['GET'])
def get_transaction(id):
    order = Order.query.get(id)
    if not Order:
        return jsonify({'message': 'Order unavailable'}), 404
    return jsonify(Order.__repr__())

@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        quantity=data['quantity'],
        product_id=data['product_id'],
        date_received=datetime.datetime.utcnow()
    )
    db.session.add(new_order)
    try:
        db.session.commit()
        return jsonify({'message': 'Order done successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/order/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'order not found'}), 404
    data = request.get_json()
    order.quantity = data['quantity']
    order.product_id = data['product_id']
    try:
        db.session.commit()
        return jsonify({'message': 'Order updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/order/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    db.session.delete(order)
    try:
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
