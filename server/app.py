#!/usr/bin/env python3

from flask import request, jsonify
from flask_restful import Resource, Api

# Local imports
from config import app, db
from models import Product

# Views go here!
api = Api(app)

@app.route('/')
def index():
    return '<h1>Inventorguard</h1>'

class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return jsonify(product.to_dict())  # Convert to dict here
            return {'error': 'Product not found'}, 404
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])  # Convert each product to dict

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
            return jsonify(new_product.to_dict()), 201  # Convert the new product to dict
        except Exception as e:
            return {'error': str(e)}, 400

api.add_resource(ProductResource, '/products', '/products/<int:product_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

