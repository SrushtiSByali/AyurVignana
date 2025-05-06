"""
AyurVignana Project Startup Script
This script helps initialize and run the AyurVignana project
"""
import os
import sys
import subprocess
import time
import webbrowser
import threading
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_header(message):
    print(f"\n{Fore.GREEN}=== {message} ==={Style.RESET_ALL}")

def print_step(message):
    print(f"{Fore.CYAN}> {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def check_mongodb():
    """Check if MongoDB is running"""
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure
        
        print_step("Checking MongoDB connection...")
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print_success("MongoDB is running!")
        return True
    except ImportError:
        print_error("pymongo package not installed. Please run: pip install pymongo")
        return False
    except ConnectionFailure:
        print_error("MongoDB is not running. Please start MongoDB first.")
        return False
    except Exception as e:
        print_error(f"MongoDB error: {str(e)}")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print_step("Checking dependencies...")
    
    requirements = ["flask", "flask_cors", "pymongo", "tensorflow", "opencv-python", "numpy", "pillow"]
    missing = []
    
    for req in requirements:
        try:
            __import__(req.replace("-", "_").split("==")[0])
        except ImportError:
            missing.append(req)
    
    if missing:
        print_error(f"Missing dependencies: {', '.join(missing)}")
        print_step("Installing missing dependencies...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print_success("Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print_error("Failed to install dependencies. Please install them manually.")
            print_step(f"Run: pip install {' '.join(missing)}")
            return False
    else:
        print_success("All dependencies are installed!")
        return True

def setup_database():
    """Initialize the database with seed data"""
    print_step("Setting up database...")
    
    try:
        # Navigate to backend directory
        os.chdir("back-end")
        
        # Run database initialization script
        process = subprocess.Popen([sys.executable, "init_db.py"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print_error(f"Database initialization failed: {stderr.decode('utf-8')}")
            return False
        
        print_success("Database initialized successfully!")
        return True
    except Exception as e:
        print_error(f"Database setup error: {str(e)}")
        return False
    finally:
        # Navigate back to original directory
        os.chdir("..")

def run_backend():
    """Run the Flask backend server"""
    print_step("Starting backend server...")
    
    try:
        # Navigate to backend directory
        os.chdir("back-end")
        
        # Run the Flask app
        if os.name == 'nt':  # Windows
            process = subprocess.Popen([sys.executable, "app.py"], 
                                      creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix-like
            process = subprocess.Popen([sys.executable, "app.py"],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        
        print_success("Backend server started!")
        
        # Give the server time to start
        time.sleep(2)
        
        # Check if server is running
        import requests
        try:
            response = requests.get("http://localhost:5000/api/health", timeout=5)
            if response.status_code == 200:
                print_success("Backend server is responding!")
            else:
                print_error(f"Backend server returned unexpected status: {response.status_code}")
        except requests.exceptions.RequestException:
            print_error("Backend server not responding. Check the console for errors.")
        
        return True
    except Exception as e:
        print_error(f"Error starting backend: {str(e)}")
        return False
    finally:
        # Navigate back to original directory
        os.chdir("..")

def serve_frontend():
    """Serve the frontend using Python's built-in HTTP server"""
    print_step("Starting frontend server...")
    
    try:
        # Navigate to frontend directory
        os.chdir("front-end")
        
        # Run the HTTP server
        if os.name == 'nt':  # Windows
            process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"], 
                                      creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix-like
            process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        
        print_success("Frontend server started at http://localhost:8080")
        return True
    except Exception as e:
        print_error(f"Error starting frontend server: {str(e)}")
        return False
    finally:
        # Navigate back to original directory
        os.chdir("..")

def open_browser():
    """Open the application in the default web browser"""
    print_step("Opening application in browser...")
    
    try:
        time.sleep(2)  # Give servers some time to start
        webbrowser.open("http://localhost:8080")
        return True
    except Exception as e:
        print_error(f"Error opening browser: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print(f"{Fore.GREEN}AyurVignana Startup Script{Style.RESET_ALL}")
    print("="*60 + "\n")
    
    # Ensure we're in the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if we're in the right directory structure
    if not os.path.exists("back-end") or not os.path.exists("front-end"):
        print_error("Script must be run from the project root directory!")
        print_step("Please place this script in the directory containing 'back-end' and 'front-end' folders")
        input("Press Enter to exit...")
        return
    
    # Sequence of startup steps
    if not check_dependencies():
        input("Press Enter to exit...")
        return
    
    if not check_mongodb():
        input("Press Enter to exit...")
        return
    
    if not setup_database():
        input("Press Enter to continue anyway (database might already be initialized)...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Start frontend
    serve_frontend()
    
    # Open application in browser
    open_browser()
    
    print("\n" + "="*60)
    print(f"{Fore.GREEN}AyurVignana is now running!{Style.RESET_ALL}")
    print("="*60)
    print(f"Backend: {Fore.CYAN}http://localhost:5000{Style.RESET_ALL}")
    print(f"Frontend: {Fore.CYAN}http://localhost:8080{Style.RESET_ALL}")
    print(f"\nPress {Fore.YELLOW}Ctrl+C{Style.RESET_ALL} to stop the application")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down AyurVignana...")

if __name__ == "__main__":
    main()