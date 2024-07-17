from datetime import datetime
from faker import Faker
from config import app, db
from models import User
from models import bcrypt

def seed_data():
    fake = Faker()
    print("Starting seed...")
    
    # Delete all records/rows in the tables
    db.session.query(User).delete()
    
    # Seed Users
    users = [
        User(email=fake.email(), company_name=fake.company(), country=fake.country(), city=fake.city()),
        User(email=fake.email(), company_name=fake.company(), country=fake.country(), city=fake.city())
    ]
    
    for user in users:
        user.set_password(fake.password())
    
    db.session.add_all(users)
    db.session.commit()

if _name_ == '_main_':
    with app.app_context():
        seed_data()