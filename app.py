from flask import Flask, request, render_template, jsonify
import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
import base64
import re

# Set up Tesseract path if it's not in your PATH environment variable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

app = Flask(__name__)

# Dictionary mapping state codes to state names
indian_states_registration = {
    "AN": "Andaman and Nicobar Islands",
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CH": "Chandigarh",
    "CG": "Chhattisgarh",
    "DD": "Daman and Diu",
    "DL": "Delhi",
    "DN": "Dadra and Nagar Haveli and Daman and Diu",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HP": "Himachal Pradesh",
    "HR": "Haryana",
    "JH": "Jharkhand",
    "JK": "Jammu and Kashmir",
    "KA": "Karnataka",
    "KL": "Kerala",
    "LD": "Lakshadweep",
    "MH": "Maharashtra",
    "ML": "Meghalaya",
    "MN": "Manipur",
    "MP": "Madhya Pradesh",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OD": "Odisha",
    "PB": "Punjab",
    "PY": "Puducherry",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TS": "Telangana",
    "TR": "Tripura",
    "UK": "Uttarakhand",
    "UP": "Uttar Pradesh",
    "WB": "West Bengal",
}

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blurred, 30, 200)
    return edged

def find_license_plate_contour(edged_image):
    contours, _ = cv2.findContours(edged_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            return approx
    return None

def mask_and_extract_plate(image, contour):
    mask = np.zeros_like(image, dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    out = np.zeros_like(image)
    out[mask == 255] = image[mask == 255]
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    cropped = image[topx:bottomx+1, topy:bottomy+1]
    return cropped

def recognize_text_from_plate(plate_image):
    gray_plate = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_plate, config='--psm 8')
    clean_text = re.sub(r'[^A-Za-z0-9]', '', text)  # Keep only alphanumeric characters
    return clean_text.strip()

def recognize_state_from_plate(plate_text):
    state_code = plate_text[:2].upper()
    return indian_states_registration.get(state_code, "Unknown State")

def process_image(image):
    edged_image = preprocess_image(image)
    license_plate_contour = find_license_plate_contour(edged_image)
    if license_plate_contour is not None:
        plate_image = mask_and_extract_plate(image, license_plate_contour)
        plate_text = recognize_text_from_plate(plate_image)
        state = recognize_state_from_plate(plate_text)
        return plate_text, state
    else:
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        image = Image.open(file.stream)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        plate_text, state = process_image(image)

        if plate_text:
            result = {
                'plate_text': plate_text,
                'state': state,
                'image': base64.b64encode(file.read()).decode('utf-8')
            }
        else:
            result = {'error': 'License plate not found'}

        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
