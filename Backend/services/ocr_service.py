import cv2
import easyocr
import os
import re
import numpy as np

# Ensure the 'uploads' folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def save_image(file):
    """Save uploaded image to the 'uploads' folder."""
    file_path = os.path.join(UPLOAD_FOLDER, "plate.jpg")
    file.save(file_path)
    return file_path

def clean_text(text):
    """Filter and correct extracted text to match Indian number plate format."""
    text = text.upper().replace(" ", "")  # Remove spaces

    # Fix common OCR misinterpretations
    text = text.replace("I", "1").replace("O", "0").replace("B", "8").replace("Z", "2")

    # Keep only alphanumeric characters
    text = "".join([char for char in text if char in ALLOWED_CHARACTERS])

    # Ensure at least 8 characters exist
    if len(text) < 8:
        return "Not detected"

    # Match Indian number plate format (relaxed check)
    match = re.search(r'([A-Z]{2,3})(\d{1,2})([A-Z]{1,3})(\d{3,4})', text)

    if match:
        formatted_plate = "".join(match.groups())
        return formatted_plate

    return "Not detected"

def preprocess_image(image_path):
    """Preprocess image to improve OCR accuracy for number plates."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding for better contrast
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 31, 2)

    # Morphological operations to remove small noise
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return morph

def extract_plate_number(image_path):
    """Extract plate number from image using EasyOCR."""
    processed_img = preprocess_image(image_path)

    # Use EasyOCR for text extraction
    reader = easyocr.Reader(['en'])
    results = reader.readtext(processed_img)

    if not results:
        return "Not detected"
    
    # Extract detected text
    extracted_text = "".join([res[1] for res in results])

    print("\U0001F50D Raw OCR Output:", extracted_text)  # Debugging

    # Force correction & restrict format
    extracted_text = clean_text(extracted_text)

    print("\u2705 Cleaned OCR Output:", extracted_text)  # Debugging

    return extracted_text
