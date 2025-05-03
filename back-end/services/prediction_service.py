"""
Service for model prediction
"""
import numpy as np
from tensorflow.keras.models import load_model
from utils.image_utils import preprocess_image
from config import Config

def predict_herb(model, preprocessed_image):
    """
    Predict herb from preprocessed image using trained model
    
    Args:
        model: Loaded Keras model
        preprocessed_image: Preprocessed image array
        
    Returns:
        tuple: (prediction_class_name, confidence_score)
    """
    # Make prediction
    predictions = model.predict(preprocessed_image)
    
    # Get the class with highest probability
    predicted_class_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class_index] * 100)
    
    # Map index to class name
    try:
        predicted_class_name = Config.CLASSES[predicted_class_index]
    except IndexError:
        # Handle case where model output doesn't match expected classes
        predicted_class_name = f"Unknown (Class {predicted_class_index})"
    
    return predicted_class_name, confidence