#!/usr/bin/env python3

# Standard library imports
from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt #pip install Flask-Bcrypt = https://pypi.org/project/Flask-Bcrypt/
from flask_cors import CORS, cross_origin #ModuleNotFoundError: No module named 'flask_cors' = pipenv install Flask-Cors
# Remote library imports
from flask import request
from flask_restful import Resource
import re

# Local imports
from config import app, db, api
# Add your model imports
from models import Product, Supplier, Order, Transaction

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])

@app.route("/users/login", methods=["POST"])
def user_login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()
    if user:
        if user.check_password(password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid password"}), 401
    else:
        return jsonify({"message": "User not found"}), 404
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)

