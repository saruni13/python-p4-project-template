from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import datetime
from flask_bcrypt import check_password_hash
import re


metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# Models go here!
    
    class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    quantity = db.Column(db.VarChar)
    price = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date_received = db.Column(DateTime, default=datetime.datetime.utcnow)
    
    product = db.relationship('Product', back_populates="orders")
    

    def __repr__(self):
        return f'<Order {self.description}, {self.description}, received on {self.date_received}>'
    
    #Employee login
    class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.Text)
    password = db.Column(db.String)
    
    
    def validate_email(self, key, email):
        # Simple regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email

    serialize_rules = ('-password',)

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)
    
    def __repr__(self):
        return f"<User {self.id}: {self.username}>"