import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import sys

def try_different_sizes(model_path, image_path):
    """Test different input sizes to find what works with the model"""
    print(f"Testing prediction with model: {model_path}")
    print(f"Using image: {image_path}")
    
    try:
        # Load the model
        model = load_model(model_path)
        print("Model loaded successfully!")
        print(f"Model input shape: {model.input_shape}")
        print(f"Model output shape: {model.output_shape}")
        
        # Try different image sizes
        test_sizes = [(128, 128), (224, 224), (160, 160), (150, 150), (200, 200)]
        
        for size in test_sizes:
            print(f"\nTrying size: {size}")
            try:
                # Load and preprocess image
                img = cv2.imread(image_path)
                if img is None:
                    print(f"Could not read image at {image_path}")
                    continue
                
                img = cv2.resize(img, size)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = img.astype(np.float32) / 255.0
                img = np.expand_dims(img, axis=0)
                
                print(f"Preprocessed image shape: {img.shape}")
                
                # Try to predict
                prediction = model.predict(img)
                print(f"Prediction successful! Output shape: {prediction.shape}")
                print(f"Successful with size: {size}")
                
                # Get predicted class
                class_idx = np.argmax(prediction[0])
                confidence = float(prediction[0][class_idx] * 100)
                print(f"Predicted class index: {class_idx}")
                print(f"Confidence: {confidence:.2f}%")
                
                # Try to get class name
                try:
                    from config import CLASSES
                    if class_idx < len(CLASSES):
                        print(f"Predicted class: {CLASSES[class_idx]}")
                except ImportError:
                    print("Could not import CLASSES from config")
                
            except Exception as e:
                print(f"Failed with size {size}: {str(e)}")
        
    except Exception as e:
        print(f"Error testing model: {str(e)}")

if __name__ == "__main__":
    # Path to model
    model_path = "./AyurVignana_prediction_cnn_.h5"
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        sys.exit(1)
    
    # Get sample image path from command line or use default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Try to find an image in the uploads folder
        uploads_dir = "./uploads"
        if os.path.exists(uploads_dir) and os.path.isdir(uploads_dir):
            files = os.listdir(uploads_dir)
            image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if image_files:
                image_path = os.path.join(uploads_dir, image_files[0])
                print(f"Using image: {image_path}")
            else:
                print("No images found in uploads folder")
                sys.exit(1)
        else:
            print("Uploads folder not found")
            sys.exit(1)
    
    # Run test with different sizes
    try_different_sizes(model_path, image_path)