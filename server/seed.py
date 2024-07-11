#!/usr/bin/env python3

# Standard library imports
# Remote library imports
# Local imports
from app import app
from faker import Faker
import datetime
import bcrypt #to seed user_password table 
from models import db, Product, Supplier, Order, Transaction, User


with app.app_context():
    fake = Faker()
        print("Starting seed...")
    
        # Seed code goes here!
        #Delete all records/rows in the columns
        Product.query.delete()
        Supplier.query.delete()
        Transaction.query.delete()
        Order.query.delete()
        User.query.delete()
        
        ## Empty lists for each table
        products[]
        suppliers[]
        transactions[]
        orders[]
        users[]
        
        #Seed Products

        #Seed Suppliers

        #Seed Orders
        orders = [
             Order(description=fake.sentence(), quantity=fake.random_int(1, 100), price=fake.random_float(), date_received=datetime.datetime.now(), product_id=1),
             Order(description=fake.sentence(), quantity=fake.random_int(1, 100), price=fake.random_float(), date_received=datetime.datetime.now() - datetime.timedelta(days=30), product_id=1),
             Order(description=fake.sentence(), quantity=fake.random_int(1, 100), price=fake.random_float(), date_received=datetime.datetime.now() - datetime.timedelta(days=60), product_id=2),
                  ]

        db.session.add_all(orders)
        db.session.commit()


        #Seed Transactions

        #Seed Users
        #The bcrypt.generate_password_hash() function takes a password as input and returns a hashed password. 
        # We then assign this hashed password to the password attribute of each User object.
        users = [
            User(name=fake.name(), email=f"{fake.email()}@example.com", role="admin"),
            User(name=fake.name(), email=f"{fake.email()}@example.com", role="supervisor"),]
        for user in users:
            user.password = bcrypt.generate_password_hash(fake.password())
            
        db.session.add_all(users)
        db.session.commit()
        print("results seeded") #we can view our seeded Users on terminal after command
  
