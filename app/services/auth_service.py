from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import mongo
from app.utils.validators import validate_email, validate_password

class AuthService:
    def signup(self, data):
        name = data.get("name", "").strip()
        email = data.get("email", "").lower().strip()
        password = data.get("password", "")

        if not name or not validate_email(email) or not validate_password(password):
            return jsonify({"message": "Invalid input"}), 400

        if mongo.db is None:
            return jsonify({"message": "Database connection error. Please check your MongoDB URI and server."}), 500

        if mongo.db.users.find_one({"email": email}):
            return jsonify({"message": "User already exists"}), 409

        hashed = generate_password_hash(password)
        mongo.db.users.insert_one({"name": name, "email": email, "password": hashed})

        token = create_access_token(identity=email)
        return jsonify({"token": token}), 201

    def login(self, data):
        email = data.get("email", "").lower().strip()
        password = data.get("password", "").strip() # Trim whitespace

        user = mongo.db.users.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return jsonify({"message": "Invalid credentials"}), 401

        token = create_access_token(identity=email)
        return jsonify({"token": token}), 200

    def get_profile(self, email):
        user = mongo.db.users.find_one({"email": email})
        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"name": user["name"], "email": user["email"]}), 200
