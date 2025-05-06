import requests
import sys

def test_backend_connection():
    """Test the connection to the backend server"""
    print("Testing connection to AyurVignana backend...")
    
    base_url = "http://localhost:5000/api"
    
    try:
        # Test health endpoint
        print(f"Testing health endpoint: {base_url}/health")
        response = requests.get(f"{base_url}/health", timeout=5)
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Backend health check successful!")
        else:
            print("❌ Backend returned an error code")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Could not connect to the backend server.")
        print("   Is the Flask server running on port 5000?")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\nIf the health check failed, follow these steps:")
    print("1. Make sure your Flask backend is running on port 5000")
    print("2. Check for any errors in the Flask server console")
    print("3. Ensure MongoDB is running and accessible")
    print("4. Verify that CORS is properly configured in the backend")

if __name__ == "__main__":
    test_backend_connection()