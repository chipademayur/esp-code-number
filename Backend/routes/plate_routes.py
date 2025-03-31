from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import easyocr
from services.plate_service import fetch_user_details, insert_plate, get_all_plates, update_user_details, delete_user_by_plate, register_user                                               

plate_bp = Blueprint("plate", __name__)

reader = easyocr.Reader(["en"])

@plate_bp.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image_np = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    results = reader.readtext(image)
    plate_number = results[0][1] if results else "Unknown"

    return jsonify(insert_plate(plate_number)), 200

@plate_bp.route("/plates", methods=["GET"])
def get_plates():
    return jsonify(get_all_plates()), 200

@plate_bp.route('/get_user/<plate_number>', methods=['GET'])
def get_user(plate_number):
    """Get user details by plate number from the database"""
    response = fetch_user_details(plate_number)
    return jsonify(response)

@plate_bp.route('/update_user/<plate_number>', methods=['PUT'])
def update_user(plate_number):
    """Update user details using plate_number"""
    updated_data = request.json  # Get JSON data from request body
    response = update_user_details(plate_number, updated_data)
    return jsonify(response)

@plate_bp.route('/delete_user/<plate_number>', methods=['DELETE'])
def delete_user(plate_number):
    response = delete_user_by_plate(plate_number)
    return jsonify(response)


@plate_bp.route('/register_user', methods=['POST'])
def register_user_api():
    try:
        data = request.json
        name = data.get('name')
        plate_number = data.get('plate_number')
        status = data.get('status')
        challan_reason = data.get('challan_reason', None)

        # Validate input
        if not name or not plate_number or not status:
            return jsonify({"message": "Missing required fields", "success": False})

        # Call service function
        response = register_user(name, plate_number, status, challan_reason)
        return jsonify(response)

    except Exception as e:
        return jsonify({"message": str(e), "success": False})

