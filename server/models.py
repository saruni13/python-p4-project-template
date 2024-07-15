from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    companyName = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)

    transactions = db.relationship('Transaction', back_populates='user')

    serialize_only = ('id', 'email', 'company_name', 'country', 'city')

    def set_password(self, plain_password):
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self.password, plain_password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_email_and_password(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    supplier_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', back_populates='product')

    serialize_only = ('id', 'name', 'sku', 'description', 'quantity', 'price', 'supplier_id', 'date')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def update_quantity(cls, product_id, quantity_change):
        product = cls.query.get(product_id)
        if product:
            product.quantity += quantity_change
            db.session.commit()
            return product
        return None

    @classmethod
    def find_all(cls):
        products = cls.query.all()
        return [product.to_dict() for product in products]

    @classmethod
    def find_low_stock(cls, threshold):
        products = cls.query.filter(cls.quantity <= threshold).all()
        return [product.to_dict() for product in products]

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='transactions')
    product = db.relationship('Product', back_populates='transactions')

    serialize_only = ('id', 'user_id', 'product_id', 'date', 'quantity', 'total_price', 'type')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_all(cls):
        transactions = cls.query.all()
        return [transaction.to_dict() for transaction in transactions]