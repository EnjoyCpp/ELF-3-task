from tensorflow.keras.models import load_model
import numpy as np
from utils import category_mapping, preprocess_image

def load_ml_model(model_path):
    """
    Load the TensorFlow model from the specified path.
    """
    try:
        model = load_model(model_path)  # Load from H5 format
        print(f"Model loaded successfully from {model_path}")
        model.summary()
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None


def get_prediction(img_array, model):
    """
    Get prediction from the model for the given image array.
    """
    if model is None:
        return {"error": "Model not loaded"}
    
    try:
        # Get prediction
        prediction = model.predict(img_array)
        
        # Process prediction based on model type
        if isinstance(prediction, list):
            prediction = prediction[0]
        
        # For classification models
        if len(prediction.shape) == 2 and prediction.shape[1] > 1:  # Multi-class
            class_idx = np.argmax(prediction, axis=1)[0]
            confidence = float(prediction[0][class_idx])
            class_name = category_mapping.get(class_idx, "Unknown")
            return {
                "class_id": int(class_idx),
                "class_name": class_name,
                "confidence": confidence
            }
        else:
            return {"raw_prediction": prediction.tolist()}
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}
