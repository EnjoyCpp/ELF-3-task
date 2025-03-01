import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO
import time
import uuid

app = Flask(__name__)
# Enable CORS with more specific settings
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

# Create upload folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = str(uuid.uuid4()) + file_ext
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        processed_path = os.path.join(PROCESSED_FOLDER, f"processed_{unique_filename}")
        
        # Save the uploaded file
        file.save(file_path)
        
        # Read the image for processing
        image = cv2.imread(file_path)
        if image is None:
            return jsonify({'error': 'Could not read image'}), 400
        
        # Example processing - replace with your actual AI model from ND1 or ND2
        # This is a placeholder - convert to grayscale and apply edge detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        # Save the processed image
        cv2.imwrite(processed_path, edges)
        
        # Convert the processed image to base64 for direct display in front-end
        with open(processed_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        # Create result JSON
        result = {
            'message': 'File processed successfully',
            'original_filename': file.filename,
            'processed_filename': f"processed_{unique_filename}",
            'image_url': f"data:image/jpeg;base64,{img_data}",
            'analysis': {
                'timestamp': time.time(),
                # Add your AI model's specific output here
                'example_detection': [
                    {'class': 'sample_object', 'confidence': 0.95, 'bbox': [10, 10, 100, 100]},
                    {'class': 'another_object', 'confidence': 0.87, 'bbox': [150, 50, 250, 150]}
                ]
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add a health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)