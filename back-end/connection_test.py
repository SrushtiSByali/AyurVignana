#!/usr/bin/env python
"""
AyurVignana Connection Test Script
This script tests all essential connections for the AyurVignana project:
- MongoDB connection test
- TensorFlow model loading test
- Flask server connection test
"""

import os
import sys
import time
import requests
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_header(message):
    print(f"\n{Fore.BLUE}=== {message} ==={Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.CYAN}i {message}{Style.RESET_ALL}")

def test_mongodb_connection():
    """Test connection to MongoDB"""
    print_header("Testing MongoDB Connection")
    
    try:
        # Import MongoDB libraries
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure
        
        # Try to connect with a short timeout
        print_info("Attempting to connect to MongoDB...")
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        
        # Test connection by issuing a simple command
        client.admin.command('ping')
        
        # Check if our database exists
        db_names = client.list_database_names()
        if "ayurvignana" in db_names:
            print_success("MongoDB connection successful!")
            print_info("The 'ayurvignana' database exists")
            
            # Check collections in the database
            db = client["ayurvignana"]
            collections = db.list_collection_names()
            if collections:
                print_info(f"Found collections: {', '.join(collections)}")
            else:
                print_info("Database exists but has no collections. Run 'python init_db.py' to initialize data.")
        else:
            print_success("MongoDB connection successful!")
            print_info("The 'ayurvignana' database does not exist yet. Run 'python init_db.py' to create it.")
        
        return True
    except ImportError:
        print_error("MongoDB driver (pymongo) is not installed")
        print_info("Install it with: pip install pymongo")
        return False
    except ConnectionFailure:
        print_error("Failed to connect to MongoDB server")
        print_info("Make sure MongoDB is running on localhost:27017")
        return False
    except Exception as e:
        print_error(f"MongoDB connection error: {str(e)}")
        return False

def test_model_loading():
    """Test TensorFlow model loading"""
    print_header("Testing TensorFlow Model Loading")
    
    try:
        # Import TensorFlow
        import tensorflow as tf
        print_info(f"TensorFlow version: {tf.__version__}")
        
        # Import our config to get model path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from config import Config
        
        model_path = Config.MODEL_PATH
        
        if not os.path.exists(model_path):
            print_error(f"Model file not found at: {model_path}")
            print_info("Make sure the model file is in the correct location")
            return False
        
        print_info(f"Loading model from: {model_path}")
        
        # Try to load the model
        model = tf.keras.models.load_model(model_path)
        
        # Get model summary
        model_summary = []
        model.summary(print_fn=lambda x: model_summary.append(x))
        
        print_success("Model loaded successfully!")
        print_info(f"Model type: {type(model).__name__}")
        print_info(f"Input shape: {model.input_shape}")
        print_info(f"Output shape: {model.output_shape}")
        
        return True
    except ImportError:
        print_error("TensorFlow is not installed")
        print_info("Install it with: pip install tensorflow")
        return False
    except Exception as e:
        print_error(f"Error loading model: {str(e)}")
        return False

def test_flask_server():
    """Test connection to Flask backend server"""
    print_header("Testing Flask Server Connection")
    
    try:
        print_info("Checking if Flask server is running...")
        response = requests.get("http://localhost:5000/api/health", timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Flask server is running and responding!")
            print_info(f"Response: {data}")
            
            # Test if predict endpoint exists (don't actually submit a prediction)
            try:
                # Just check if the endpoint responds to an OPTIONS request
                options_response = requests.options("http://localhost:5000/api/predict", timeout=2)
                if options_response.status_code < 400:  # Any non-error code
                    print_success("Prediction endpoint exists")
                else:
                    print_error("Prediction endpoint returned error status")
            except:
                print_info("Could not verify prediction endpoint")
            
            return True
        else:
            print_error(f"Flask server returned error status: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to Flask server at http://localhost:5000")
        print_info("Make sure the Flask server is running (python app.py)")
        return False
    except requests.exceptions.Timeout:
        print_error("Connection to Flask server timed out")
        print_info("The server might be starting up or under heavy load")
        return False
    except Exception as e:
        print_error(f"Error testing Flask server: {str(e)}")
        return False

def run_all_tests():
    """Run all connection tests"""
    print("\n" + "="*60)
    print(f"{Fore.GREEN}AyurVignana Connection Test{Style.RESET_ALL}")
    print("="*60)
    
    # Run all tests
    mongo_ok = test_mongodb_connection()
    model_ok = test_model_loading()
    flask_ok = test_flask_server()
    
    # Print summary
    print("\n" + "="*60)
    print(f"{Fore.GREEN}Connection Test Summary{Style.RESET_ALL}")
    print("="*60)
    
    print(f"MongoDB Connection: {'✓ PASS' if mongo_ok else '✗ FAIL'}")
    print(f"TensorFlow Model:   {'✓ PASS' if model_ok else '✗ FAIL'}")
    print(f"Flask Server:       {'✓ PASS' if flask_ok else '✗ FAIL'}")
    
    print("\n" + "-"*60)
    if mongo_ok and model_ok and flask_ok:
        print(f"{Fore.GREEN}All connections are working correctly!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Some connections have issues. Please fix them before proceeding.{Style.RESET_ALL}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    run_all_tests()