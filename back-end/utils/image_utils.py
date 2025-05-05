import cv2
import numpy as np
import tensorflow as tf
from config import Config

def preprocess_image(image_path):
    """
    Preprocess image for prediction using the correct dimensions and format
    based on the model diagnostic results.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        numpy.ndarray: Preprocessed image ready for model prediction
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    # Model expects 128x128 RGB images
    img = cv2.resize(img, (128, 128))  # Resize to correct dimensions
    
    # Convert BGR to RGB (since model was likely trained on RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Apply CLAHE for contrast enhancement if needed (optional)
    # lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    # l, a, b = cv2.split(lab)
    # clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    # l = clahe.apply(l)
    # img = cv2.merge((l, a, b))
    # img = cv2.cvtColor(img, cv2.COLOR_LAB2RGB)
    
    # Scale pixel values to [0, 1]
    img = img.astype(np.float32) / 255.0
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    
    print(f"Preprocessed image shape: {img.shape}")
    return img
