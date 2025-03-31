from flask import Blueprint, request, jsonify
from services.admin_service import authenticate_admin
from werkzeug.security import generate_password_hash
from services.admin_service import register_admin
from flask_cors import CORS

admin_bp = Blueprint("admin", __name__)
CORS(admin_bp) 

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Username and password are required", "success": False}), 400

        response = authenticate_admin(username, password)
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500

@admin_bp.route("/register_admin", methods=["POST"])
def register_admin_api():
    """Register a new admin"""
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Missing username or password", "success": False}), 400

        hashed_password = generate_password_hash(password)

        response = register_admin(username, hashed_password)
        return jsonify(response)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500