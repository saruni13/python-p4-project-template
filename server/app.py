#!/usr/bin/env python3

from flask import Flask, request, jsonify, abort
from config import app, db
from flask_migrate import Migrate
from models import  User
from flask_bcrypt import Bcrypt
import datetime

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Project Group 5</h1>'

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # Return a list of all users
        users = User.query.all()
        return jsonify([user.serialize for user in users])
    elif request.method == 'POST':
        # Create a new user
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        company_name = data.get('company_name')
        country = data.get('country')
        city = data.get('city')

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "User already exists"}), 400

        new_user = User(
            email=email,
            company_name=company_name,
            country=country,
            city=city
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Login successful", "user_id": user.id})
    else:
        return jsonify({"message": "Invalid email or password"}), 401

if _name_ == '_main_':
    app.run(port=5555, debug=True)