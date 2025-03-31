from config.db import get_db_connection

def insert_plate(number):
    db = get_db_connection()
    cursor = db.cursor()
    sql = "INSERT INTO plates (number) VALUES (%s)"
    cursor.execute(sql, (number,))
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Plate added", "plate": number}

def get_all_plates():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    plates = cursor.fetchall()
    cursor.close()
    db.close()
    return plates

def fetch_user_details(plate_number):
    """Fetch user details from the database based on plate_number"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Dictionary cursor for JSON response
        query = "SELECT * FROM users WHERE plate_number = %s"
        cursor.execute(query, (plate_number,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return {"success": True, "data": user}
        else:
            return {"success": False, "message": "User not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_user_details(plate_number, updated_data):
    """Update user details in the database based on plate_number"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch current user details
        cursor.execute("SELECT * FROM users WHERE plate_number = %s", (plate_number,))
        existing_user = cursor.fetchone()

        if not existing_user:
            return {"success": False, "message": "User not found"}

        print("Existing User Data:", existing_user)  # Debugging step

        # Dynamically build the SET part of the query
        set_clauses = []
        values = []
        
        for key, value in updated_data.items():
            if str(existing_user.get(key)) != str(value):  # Compare old and new values
                set_clauses.append(f"{key} = %s")
                values.append(value)

        if not set_clauses:
            return {"success": False, "message": "No changes detected"}

        values.append(plate_number)  # Add plate_number to values list for WHERE clause

        query = f"UPDATE users SET {', '.join(set_clauses)} WHERE plate_number = %s"
        cursor.execute(query, tuple(values))
        conn.commit()

        # 🔥 **Manually check if the data is updated**
        cursor.execute("SELECT * FROM users WHERE plate_number = %s", (plate_number,))
        updated_user = cursor.fetchone()

        cursor.close()
        conn.close()

        if updated_user == existing_user:
            return {"success": False, "message": "No changes detected, same data"}

        return {"success": True, "message": "User details updated successfully", "updated_data": updated_user}

    except Exception as e:
        return {"success": False, "error": str(e)}
def delete_user_by_plate(plate_number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE plate_number = %s", (plate_number,))
        user = cursor.fetchone()
        if not user:
            return {"message": "User not found", "success": False}

        # Delete the user
        cursor.execute("DELETE FROM users WHERE plate_number = %s", (plate_number,))
        conn.commit()

        return {"message": "User deleted successfully", "success": True}

    except Exception as e:
        return {"message": str(e), "success": False}

    finally:
        cursor.close()
        conn.close()
def register_user(name, plate_number, status, challan_reason):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if plate_number already exists
    cursor.execute("SELECT * FROM users WHERE plate_number = %s", (plate_number,))
    existing_user = cursor.fetchone()

    if existing_user:
        return {"message": "User with this plate number already exists", "success": False}

    # Insert new user
    query = "INSERT INTO users (name, plate_number, status, challan_reason) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, plate_number, status, challan_reason))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "User registered successfully", "success": True}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   