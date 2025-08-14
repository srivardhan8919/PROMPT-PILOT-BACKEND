from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
auth = AuthService()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    return auth.signup(data)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return auth.login(data)

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    return auth.get_profile(current_user)
