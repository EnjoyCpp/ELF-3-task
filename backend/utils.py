import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image

# Category mapping from class ID to class name
category_mapping = {
    0: 'actinic keratosis',              
    1: 'basal cell carcinoma',          
    2: 'dermatofibroma',               
    3: 'melanoma',                 
    4: 'nevus',                         
    5: 'pigmented benign keratosis',    
    6: 'seborrheic keratosis',     
    7: 'squamous cell carcinoma',         
    8: 'vascular lesion',           
}

def preprocess_image(img_path, target_size=(224, 224)):
    """
    Preprocess image for model prediction.
    """
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize pixel values
    img_array = img_array / 255.0  
    return img_array


def visualize_prediction(image_cv, prediction_result):
    """
    Visualize the prediction results on the image.
    """
    vis_image = image_cv.copy()
    
    if "class_id" in prediction_result:
        # Add a larger text size for the class and confidence
        text = f"{prediction_result.get('class_name')}: {prediction_result.get('confidence'):.2f}"
        cv2.putText(vis_image, text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    
    return vis_image
