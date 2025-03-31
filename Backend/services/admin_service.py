from config.db import get_db_connection
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash


def authenticate_admin(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM admin WHERE username = %s"
        cursor.execute(query, (username,))
        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if not admin:
            return {"message": "Invalid credentials", "success": False}

        # Use check_password_hash to verify the password
        if check_password_hash(admin["password"], password):
            return {"message": "Login successful", "success": True, "admin": {"username": admin["username"]}}
        else:
            return {"message": "Invalid credentials", "success": False}

    except Exception as e:
        return {"message": str(e), "success": False}


def register_admin(username, hashed_password):
    """Register a new admin in the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the admin already exists
        cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
        existing_admin = cursor.fetchone()

        if existing_admin:
            return {"message": "Admin with this username already exists", "success": False}

        # Insert new admin
        query = "INSERT INTO admin (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Admin registered successfully", "success": True}

    except Exception as e:
        return {"message": str(e), "success": False}