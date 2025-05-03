"""
Diagnostic script to test AyurVignana backend components
Run this to check if all parts of the backend are working properly
"""
import os
import sys
import requests
import importlib
import time
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}! {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.CYAN}i {message}{Style.RESET_ALL}")

def print_header(message):
    print(f"\n{Fore.BLUE}=== {message} ==={Style.RESET_ALL}")

def check_dependencies():
    print_header("Checking Python Dependencies")
    
    dependencies = [
        "flask", 
        "flask_cors", 
        "pymongo", 
        "tensorflow", 
        "cv2", 
        "numpy", 
        "PIL"
    ]
    
    missing_deps = []
    
    for dep in dependencies:
        try:
            if dep == "cv2":
                importlib.import_module("cv2")
            elif dep == "PIL":
                importlib.import_module("PIL")
            else:
                importlib.import_module(dep)
            
            print_success(f"{dep} is installed")
        except ImportError:
            print_error(f"{dep} is NOT installed")
            if dep == "cv2":
                missing_deps.append("opencv-python")
            elif dep == "PIL":
                missing_deps.append("pillow")
            else:
                missing_deps.append(dep)
    
    if missing_deps:
        print_warning("\nMissing dependencies. Install with:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    
    print_success("All dependencies are installed")
    return True

def check_mongodb_connection():
    print_header("Checking MongoDB Connection")
    
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure
        
        # Try to connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Test connection
        
        # Check if the ayurvignana database exists
        db_names = client.list_database_names()
        if "ayurvignana" in db_names:
            print_success("Connected to MongoDB and 'ayurvignana' database exists")
        else:
            print_warning("Connected to MongoDB but 'ayurvignana' database doesn't exist")
            print_info("Run 'python init_db.py' to initialize the database")
        
        return True
    except ConnectionFailure:
        print_error("Failed to connect to MongoDB. Is MongoDB running?")
        return False
    except Exception as e:
        print_error(f"MongoDB check failed: {str(e)}")
        return False

def check_model_file():
    print_header("Checking ML Model File")
    
    # Import config to get the model path
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from config import Config
        
        model_path = Config.MODEL_PATH
        
        if os.path.exists(model_path):
            print_success(f"Model file found at: {model_path}")
            
            # Check if tensorflow can load it
            try:
                import tensorflow as tf
                model = tf.keras.models.load_model(model_path)
                print_success("Model loaded successfully with TensorFlow")
                return True
            except Exception as e:
                print_error(f"Model exists but could not be loaded: {str(e)}")
                return False
        else:
            print_error(f"Model file not found at: {model_path}")
            print_info("Make sure the model file is in the correct location")
            return False
            
    except Exception as e:
        print_error(f"Error checking model file: {str(e)}")
        return False

def check_flask_server():
    print_header("Checking Flask Server")
    
    try:
        # Check if Flask server is running
        response = requests.get("http://localhost:5000/api/health", timeout=2)
        
        if response.status_code == 200:
            print_success("Flask server is running and health endpoint is accessible")
            health_data = response.json()
            print_info(f"API Status: {health_data.get('status')}")
            return True
        else:
            print_error(f"Flask server returned unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to Flask server. Is it running?")
        print_info("Start the server with 'python app.py'")
        return False
    except Exception as e:
        print_error(f"Error checking Flask server: {str(e)}")
        return False

def check_static_uploads_folder():
    print_header("Checking Static Uploads Folder")
    
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from config import Config
        
        upload_folder = Config.UPLOAD_FOLDER
        
        if os.path.exists(upload_folder):
            print_success(f"Upload folder exists at: {upload_folder}")
            
            # Test if it's writable
            try:
                test_file = os.path.join(upload_folder, "test_write.txt")
                with open(test_file, "w") as f:
                    f.write("Test")
                os.remove(test_file)
                print_success("Upload folder is writable")
                return True
            except Exception as e:
                print_error(f"Upload folder exists but is not writable: {str(e)}")
                return False
        else:
            print_warning(f"Upload folder doesn't exist at: {upload_folder}")
            print_info("Creating upload folder...")
            
            try:
                os.makedirs(upload_folder, exist_ok=True)
                print_success("Upload folder created successfully")
                return True
            except Exception as e:
                print_error(f"Failed to create upload folder: {str(e)}")
                return False
    except Exception as e:
        print_error(f"Error checking upload folder: {str(e)}")
        return False

def main():
    print("\n" + "="*50)
    print(f"{Fore.GREEN}AyurVignana Backend Diagnostic Tool{Style.RESET_ALL}")
    print("="*50 + "\n")
    
    # Run all tests
    deps_ok = check_dependencies()
    mongo_ok = check_mongodb_connection()
    model_ok = check_model_file()
    uploads_ok = check_static_uploads_folder()
    
    # Optionally check Flask server if other tests pass
    flask_ok = False
    if deps_ok and mongo_ok and model_ok:
        print_info("\nAttempting to check Flask server (if running)...")
        flask_ok = check_flask_server()
    
    # Print summary
    print("\n" + "="*50)
    print(f"{Fore.GREEN}Diagnostic Summary{Style.RESET_ALL}")
    print("="*50)
    
    print(f"Dependencies: {'✓' if deps_ok else '✗'}")
    print(f"MongoDB Connection: {'✓' if mongo_ok else '✗'}")
    print(f"ML Model: {'✓' if model_ok else '✗'}")
    print(f"Uploads Folder: {'✓' if uploads_ok else '✗'}")
    print(f"Flask Server: {'✓' if flask_ok else '✗'}")
    
    # Overall status
    print("\n" + "-"*50)
    if deps_ok and mongo_ok and model_ok and uploads_ok:
        print(f"{Fore.GREEN}Backend setup is correctly configured!{Style.RESET_ALL}")
        if not flask_ok:
            print_info("Flask server is not running. Start it with 'python app.py'")
    else:
        print(f"{Fore.RED}Backend has issues that need to be fixed.{Style.RESET_ALL}")
        print_info("Fix the issues indicated above and run this diagnostic again.")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()