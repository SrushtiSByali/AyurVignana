import numpy as np
from config import Config

def predict_herb(model, preprocessed_image):
    """
    Use the loaded model to predict herb type from preprocessed image.
    Handles the class mismatch between model output (118) and Config.CLASSES (117).
    
    Args:
        model: Loaded TensorFlow model
        preprocessed_image: Preprocessed image array
        
    Returns:
        tuple: (predicted_herb_name, confidence_percentage)
    """
    try:
        # Make prediction
        predictions = model.predict(preprocessed_image)
        
        # Print prediction shape for debugging
        print(f"Raw prediction shape: {predictions.shape}")
        
        # Get the predicted class index
        predicted_class_index = np.argmax(predictions[0])
        print(f"Predicted class index: {predicted_class_index}")
        
        # Get the confidence score
        confidence = float(predictions[0][predicted_class_index] * 100)
        print(f"Confidence: {confidence:.2f}%")
        
        # Handle the class mismatch (model has 118 classes, Config.CLASSES might have 117)
        num_classes = len(Config.CLASSES)
        
        if predicted_class_index < num_classes:
            # We have this class in our config
            predicted_herb = Config.CLASSES[predicted_class_index]
        else:
            # This is the "extra" class not in our config
            predicted_herb = f"Unknown (Class {predicted_class_index})"
            
            # If you added "Unknown" as the 118th class in Config.CLASSES, uncomment:
            # if predicted_class_index < len(Config.CLASSES):
            #     predicted_herb = Config.CLASSES[predicted_class_index]
        
        print(f"Predicted herb: {predicted_herb}")
        return predicted_herb, confidence
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        raise
