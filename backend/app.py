from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import time
import os
import base64
import cv2

from model import load_ml_model, get_prediction
from utils import preprocess_image, visualize_prediction, category_mapping

import logging

# Flask application setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", 
                             "methods": ["GET", "POST", "OPTIONS"], 
                             "allow_headers": ["Content-Type", "Authorization"]}})

# Configuration constants
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
MODEL_PATH = 'model.h5'

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Load the model at startup
model = load_ml_model(MODEL_PATH)

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    """
    Handle image upload, process it with the model, and return results.
    Supports CORS preflight OPTIONS requests.
    """
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    # Validate request
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the original image with a unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = str(uuid.uuid4()) + file_ext
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        processed_path = os.path.join(PROCESSED_FOLDER, f"processed_{unique_filename}")
        file.save(file_path)
        
        logging.info(f"File saved successfully to {file_path}")

        # Read the image and get prediction
        processed_img = preprocess_image(file_path)
        logging.info(f"Image preprocessed successfully")
        
        prediction_result = get_prediction(processed_img, model)
        logging.info(f"Prediction result: {prediction_result}")

        # Visualize the prediction on the image
        image_cv = cv2.imread(file_path)
        processed_image = visualize_prediction(image_cv, prediction_result)
        logging.info(f"Prediction visualized on image")

        # Save the processed image
        cv2.imwrite(processed_path, processed_image)
        logging.info(f"Processed image saved to {processed_path}")

        # Convert the processed image to base64 for front-end display
        with open(processed_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        logging.info(f"Processed image converted to base64")

        # Create and return result JSON
        result = {
            'message': 'File processed successfully',
            'original_filename': file.filename,
            'processed_filename': f"processed_{unique_filename}",
            'image_url': f"data:image/jpeg;base64,{img_data}",
            'analysis': {
                'timestamp': time.time(),
                'model_prediction': prediction_result
            }
        }

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify service and model status.
    """
    model_status = "loaded" if model is not None else "not loaded"
    return jsonify({
        'status': 'healthy', 
        'model_status': model_status
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
