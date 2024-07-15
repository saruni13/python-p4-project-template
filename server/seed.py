#!/usr/bin/env python3

from app import app
from faker import Faker
import datetime
from models import db, Product, Transaction, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

with app.app_context():
    fake = Faker()
    print("Starting seed...")
    
    # Delete all records/rows in the tables
    Product.query.delete()
    Transaction.query.delete()
    User.query.delete()
    
    # Seed Users
    users = [
        User(email=fake.email(), company_name=fake.company(), country=fake.country(), city=fake.city()),
        User(email=fake.email(), company_name=fake.company(), country=fake.country(), city=fake.city())
    ]
    
    for user in users:
        user.set_password(fake.password())
    
    db.session.add_all(users)
    db.session.commit()

    # Seed Products
    products = [
        Product(name=fake.word(), sku=fake.uuid4(), description=fake.sentence(), quantity=fake.random_int(min=1, max=100), price=fake.random_number(digits=4, fix_len=True), supplier_id=fake.random_int(min=1, max=10), date=datetime.datetime.now()),
        Product(name=fake.word(), sku=fake.uuid4(), description=fake.sentence(), quantity=fake.random_int(min=1, max=100), price=fake.random_number(digits=4, fix_len=True), supplier_id=fake.random_int(min=1, max=10), date=datetime.datetime.now() - datetime.timedelta(days=30)),
        Product(name=fake.word(), sku=fake.uuid4(), description=fake.sentence(), quantity=fake.random_int(min=1, max=100), price=fake.random_number(digits=4, fix_len=True), supplier_id=fake.random_int(min=1, max=10), date=datetime.datetime.now() - datetime.timedelta(days=60))
    ]
    
    db.session.add_all(products)
    db.session.commit()
    
    # Seed Transactions
    transactions = [
        Transaction(user_id=users[0].id, product_id=products[0].id, quantity=fake.random_int(min=1, max=100), total_price=fake.random_number(digits=5, fix_len=True), type='purchase', date=datetime.datetime.now()),
        Transaction(user_id=users[1].id, product_id=products[1].id, quantity=fake.random_int(min=1, max=100), total_price=fake.random_number(digits=5, fix_len=True), type='purchase', date=datetime.datetime.now() - datetime.timedelta(days=30)),
        Transaction(user_id=users[0].id, product_id=products[2].id, quantity=fake.random_int(min=1, max=100), total_price=fake.random_number(digits=5, fix_len=True), type='purchase', date=datetime.datetime.now() - datetime.timedelta(days=60))
    ]
    
    db.session.add_all(transactions)
    db.session.commit()

    print("Database seeded successfully!")