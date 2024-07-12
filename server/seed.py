#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from datetime import datetime
from config import db
from models import Product, Supplier, Transaction, Order

# Remote library imports
from faker import Faker

# Local imports
from app import app

fake = Faker()

def create_suppliers():
    suppliers = [
        Supplier(name=fake.company(), description=fake.catch_phrase(), created_at=datetime.utcnow()) for _ in range(5)
    ]
    db.session.add_all(suppliers)
    db.session.commit()
    return suppliers

def create_products(suppliers):
    products = [
        Product(name=fake.product_name(), description=fake.text(), price=randint(50, 200), supplier_id=rc(suppliers).id, created_at=datetime.utcnow()) for _ in range(10)
    ]
    db.session.add_all(products)
    db.session.commit()
    return products

def create_transactions(products):
    transactions = [
        Transaction(quantity=randint(1, 100), product_id=rc(products).id, created_at=datetime.utcnow()) for _ in range(20)
    ]
    db.session.add_all(transactions)
    db.session.commit()
    return transactions

def create_orders(products):
    orders = [
        Order(description=fake.text(), quantity=randint(1, 50), price=randint(50, 200), product_id=rc(products).id, created_at=datetime.utcnow()) for _ in range(15)
    ]
    db.session.add_all(orders)
    db.session.commit()
    return orders

if __name__ == '__main__':
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        print("Creating suppliers...")
        suppliers = create_suppliers()
        print("Creating products...")
        products = create_products(suppliers)
        print("Creating transactions...")
        transactions = create_transactions(products)
        print("Creating orders...")
        orders = create_orders(products)

        print("Database seeded!")
