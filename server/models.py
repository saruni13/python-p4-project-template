from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import DateTime, ForeignKey
import datetime

from config import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)

    products = db.relationship('Product', back_populates='supplier')

    def __repr__(self):
        return f'<Supplier {self.id}, {self.name}, {self.description}, {self.date}>'

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.String)
    supplier_id = db.Column(db.Integer, ForeignKey('suppliers.id'))
    date = db.Column(DateTime, default=datetime.datetime.utcnow)

    supplier = db.relationship('Supplier', back_populates='products')
    transactions = db.relationship('Transaction', back_populates='product')

    def __repr__(self):
        return f'<Product {self.id}, {self.name}, {self.description}, {self.price}, {self.supplier_id}, {self.date}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, ForeignKey('products.id'))
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)

    product = db.relationship('Product', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction {self.id}, {self.quantity}, {self.product_id}, {self.created_at}>'