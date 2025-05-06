import cv2
import numpy as np
import tensorflow as tf
from config import Config, CLASSES
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input

def preprocess_image(image_path):
    """
    Preprocess image for prediction using the correct dimensions and format
    for the AyurVignana_prediction_cnn_.h5 model.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        numpy.ndarray: Preprocessed image ready for model prediction
    """
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")
        
        # Get original dimensions for debugging
        original_height, original_width, channels = img.shape
        print(f"Original image shape: {img.shape}")
        
        # Resize to match the CNN model's expected input
        # For CNN models, this is typically 224x224
        img = cv2.resize(img, Config.IMG_SIZE)
        print(f"Resized to: {img.shape}")
        
        # Convert BGR to RGB (since model was likely trained on RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Scale pixel values to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        print(f"Preprocessed image shape: {img.shape}")
        return img

    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        raise

def predict_herb(model, preprocessed_image):
    """
    Predict herb from preprocessed image using the loaded model
    
    Args:
        model: Loaded Keras model
        preprocessed_image: Numpy array of preprocessed image
        
    Returns:
        tuple: (predicted_herb_name, confidence_percentage)
    """
    try:
        # Make prediction
        predictions = model.predict(preprocessed_image)
        
        # Get the predicted class index and confidence
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_index] * 100)
        
        # Get the predicted class name
        predicted_herb = CLASSES[predicted_class_index]
        
        return predicted_herb, confidence
        
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        raise Exception(f"Prediction failed: {str(e)}")