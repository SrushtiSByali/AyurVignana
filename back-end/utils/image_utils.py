"""
Utility functions for image processing
"""
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from config import Config

def preprocess_image(image_path):
    """
    Preprocess an image for model prediction
    
    Args:
        image_path: Path to the image file
        
    Returns:
        numpy.ndarray: Preprocessed image as a numpy array ready for model prediction
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    # Convert to RGB (OpenCV uses BGR by default)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize to the expected input size
    img = cv2.resize(img, Config.IMG_SIZE)
    
    # Convert to array and normalize
    img_array = img_to_array(img)
    img_array = img_array / 255.0  # Normalize to [0,1]
    
    # Expand dimensions to match model's expected input
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array