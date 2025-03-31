from flask import Blueprint, request, jsonify
from services.ocr_service import save_image, extract_plate_number
from services.plate_service import fetch_user_details
from flask_cors import CORS

ocr_bp = Blueprint('ocr_bp', __name__)
CORS(ocr_bp)

@ocr_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded", "success": False}), 400
    
    file = request.files['file']
    image_path = save_image(file)
    
    plate_number = extract_plate_number(image_path)
    user_details = fetch_user_details(plate_number)
    
    return jsonify({
        "message": "Image received",
        "plate_number": plate_number,
        "user_details": user_details,
        "success": True
    })
