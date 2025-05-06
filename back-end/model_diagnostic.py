import os
import sys
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model

def diagnose_model(model_path):
    """
    Diagnose CNN model structure and input/output shapes
    """
    print(f"Diagnosing CNN model at: {model_path}")
    
    try:
        # Load the model
        model = load_model(model_path)
        print("Model loaded successfully!")
        
        # Print model summary
        model.summary()
        
        # Get model input shape
        input_shape = model.input_shape
        print(f"Model input shape: {input_shape}")
        
        # Get model output shape
        output_shape = model.output_shape
        print(f"Model output shape: {output_shape}")
        
        # Get number of classes
        num_classes = output_shape[-1]
        print(f"Number of classes: {num_classes}")
        
        # Get first dense layer for diagnostics
        dense_layers = [layer for layer in model.layers if 'dense' in layer.name]
        if dense_layers:
            first_dense = dense_layers[0]
            print(f"First dense layer name: {first_dense.name}")
            
            # Try to get input shape expected by first dense layer
            try:
                if hasattr(first_dense, 'input_spec'):
                    print(f"First dense layer expected input shape: {first_dense.input_spec.shape}")
                elif hasattr(first_dense, '_batch_input_shape'):
                    print(f"First dense layer expected input shape: {first_dense._batch_input_shape}")
            except Exception as e:
                print(f"Error diagnosing model: {str(e)}")
        
        # Test prediction with random input
        print("\nTesting prediction with random input:")
        if input_shape[1] is not None and input_shape[2] is not None and input_shape[3] is not None:
            random_input = np.random.random((1, input_shape[1], input_shape[2], input_shape[3]))
            print(f"Random input shape: {random_input.shape}")
            
            try:
                prediction = model.predict(random_input)
                print(f"Prediction shape: {prediction.shape}")
                print(f"Max class index: {np.argmax(prediction[0])}")
                print("Prediction test successful!")
            except Exception as e:
                print(f"Prediction test failed: {str(e)}")
        
        return True
    
    except Exception as e:
        print(f"Model diagnosis failed. Please check the model file.")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    model_path = "./AyurVignana_prediction_cnn_.h5"
    
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    
    if not os.path.exists(model_path):
        print(f"Model file not found at: {model_path}")
        sys.exit(1)
    
    success = diagnose_model(model_path)
    
    if success:
        print("\nModel diagnosis completed successfully.")
    else:
        print("\nModel diagnosis failed.")