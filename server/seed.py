#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from datetime import datetime
from config import db
from models import Product, Supplier, Transaction

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db

db.create_all()

# supplier1=Supplier(
#     name='TechComp',
#     description='Supplier of high end computer products'
#     date=datetime.now()
#     )


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
