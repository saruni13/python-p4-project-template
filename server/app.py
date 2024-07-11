#!/usr/bin/env python3

from flask import request, jsonify
from flask_restful import Resource, Api

# Local imports
from config import app, db
from models import Product, Supplier, Transaction

# Views go here!
api = Api(app)

@app.route('/')
def index():
    return '<h1>Adida Barack Pilly</h1>'
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
                suppliers_id=data["suppliers_id"],
                created_at=data["created_at"]
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
            if Supplier:
                return jsonify(supplier.to_dict())
            return{'error': "Supplier not found!"}
        suppliers = Supplier.query.all()
        return jsonify([supplier.to_dict() for supplier in suppliers])
    

    def post(self):
        data = request.get_json()
        try:
            new_supplier = Supplier(
                name=data["name"],
                description=data["description"],
                created_at=data["created_at"]
            )

            db.session.add(new_supplier)
            db.session.commit()
            return jsonify(new_supplier.to_dict()), 201
        except Exception as e:
            return {'error': str(e)}, 400

class TransactionsResource(Resource):
    def get(self, transaction_id=None):
        if transaction_id:
            transaction = Transaction.query.all()
            if Transaction:
                return jsonify(transaction.to_dict())
            return{'error': "Transaction not found!"}
        transactions = Transaction.query.all()
        return jsonify([transaction.to_dict() for transaction in transactions])
    
    def post(self):
        data = request.get_json()
        try:
            new_transaction = Transaction(
                quantity = data["quantity"],
                product_id = data["product_id"],
                created_at = data["created_at"]
            )

            db.session.add(new_transaction)
            db.session.commit()
            return jsonify(new_transaction.to_dict()), 201
        except Exception as e:
            return {'error': str(e)}, 400

api.add_resource(ProductResource, '/products', '/products/<int:product_id>')
api.add_resource(SupplierResource, '/suppliers', '/suppliers/<int:supplier_id>')
api.add_resource(TransactionsResource, '/transactions', '/transactions/<int:transaction_id>')

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)

