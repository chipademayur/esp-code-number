import cv2
import numpy as np
import pytesseract
import easyocr
import os
import re

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
    text = text.upper()

    # Fix common OCR misinterpretations
    text = text.replace("I", "1").replace("O", "0").replace("B", "8").replace("Z", "2")

    # Ensure first two characters are letters, not numbers
    if len(text) >= 10:
        if text[0] in "0123456789":
            text = "M" + text[1:]  # If first character is a number, replace it with 'M'
        if text[1] in "0123456789":
            text = text[0] + "H" + text[2:]  # If second character is a number, replace it with 'H'

    # Keep only allowed alphanumeric characters
    text = "".join([char for char in text if char in ALLOWED_CHARACTERS])

    # Ensure at least 10 characters exist
    if len(text) < 10:
        return "Not detected"

    # Match Indian number plate format: 2 letters, 2 digits, 2 letters, 4 digits
    match = re.search(r'([A-Z]{2})(\d{2})([A-Z]{2})(\d{4})', text)

    if match:
        return "".join(match.groups())

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

def extract_text(image_path):
    """Extract plate number from image using EasyOCR and enforce strict format."""
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
