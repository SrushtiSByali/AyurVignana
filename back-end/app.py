from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import sys

try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    print(f"TensorFlow version: {tf.__version__}")
except ImportError as e:
    print("Error importing TensorFlow:", e)
    sys.exit(1)

from services.prediction_service import predict_herb
from services.herb_service import get_herb_by_name, get_recommendations_by_symptoms, seed_database
from utils.image_utils import preprocess_image
from pymongo import MongoClient
from config import Config

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Load configuration
app.config.from_object(Config)

# Connect to MongoDB
try:
    client = MongoClient(app.config['MONGO_URI'])
    db = client[app.config['MONGO_DB_NAME']]
    
    # Test connection
    client.server_info()
    print("Successfully connected to MongoDB")
    
    # Seed database if it's empty
    if db.herbs.count_documents({}) == 0:
        print("Seeding database with initial data...")
        seed_database(db)
        
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")
    print("Starting app without database connection.")
    db = None

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the trained model
try:
    model_path = app.config['MODEL_PATH']
    if os.path.exists(model_path):
        model = load_model(model_path)
        print(f"Model loaded successfully from {model_path}")
    else:
        print(f"Model file not found at {model_path}")
        model = None
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "message": "AyurVignana API is running",
        "database": "connected" if db is not None else "disconnected",
        "model": "loaded" if model is not None else "not loaded"
    }
    return jsonify(status)

@app.route('/api/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint to predict herb from uploaded image"""
    # Check if model is loaded
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    # Check for file in request
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    
    print(f"Received image: {file.filename}")
    
    # Check file extension
    extension = file.filename.split('.')[-1].lower()
    if extension not in app.config['ALLOWED_EXTENSIONS']:
        return jsonify({"error": f"File extension '{extension}' not allowed"}), 400
    
    # Save the uploaded image
    try:
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"Saved image to {file_path}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return jsonify({"error": f"Could not save file: {str(e)}"}), 500
    

    # Connect to MongoDB
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client[app.config['MONGO_DB_NAME']]
    
        # Test connection
        client.server_info()
        print("Successfully connected to MongoDB")
    
        # Seed database if it's empty
        # Fix: Use count_documents({}) > 0 instead of bool check
        if db.herbs.count_documents({}) == 0:
            print("Seeding database with initial data...")
            seed_database(db)
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        print("Starting app without database connection.")
        db = None

    try:
        # Preprocess image and predict
        processed_image = preprocess_image(file_path)
        prediction, confidence = predict_herb(model, processed_image)
        
        print(f"Predicted herb: {prediction} with confidence {confidence}%")
        
        # If database is not connected, return simplified response
        if db is None:
            return jsonify({
                "name": prediction,
                "scientific": "N/A (Database not connected)",
                "nature": "N/A",
                "dosha": "N/A",
                "description": "Database connection is required for detailed information.",
                "confidence": confidence,
                "image_url": f"/api/uploads/{filename}"
            })
        
        # Get herb details from database
        herb_details = get_herb_by_name(db, prediction)
        
        if not herb_details:
            # Return prediction even if herb details not found
            return jsonify({
                "name": prediction,
                "scientific": "Not found in database",
                "nature": "Unknown",
                "dosha": "Unknown",
                "description": "This herb was identified but details are not available in the database.",
                "confidence": confidence,
                "image_url": f"/api/uploads/{filename}"
            })
        
        # Format response
        response = {
            "name": herb_details["name"],
            "scientific": herb_details["scientific_name"],
            "nature": herb_details["nature"],
            "dosha": herb_details["dosha_compatibility"],
            "description": herb_details["description"],
            "confidence": confidence,
            "image_url": f"/api/uploads/{filename}"
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Endpoint to get herb recommendations based on symptoms"""
    # Check database connection
    if db is None:
        return jsonify({
            "error": "Database not connected",
            "recommendations": []
        }), 500
    
    # Check request data
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.json
    if not data or 'symptoms' not in data:
        return jsonify({"error": "No symptoms provided"}), 400
    
    symptoms = data['symptoms'].lower()
    print(f"Searching recommendations for symptoms: {symptoms}")
    
    try:
        # Get recommendations from database
        recommendations = get_recommendations_by_symptoms(db, symptoms)
        
        print(f"Found {len(recommendations)} recommendations")
        return jsonify({"recommendations": recommendations})
    
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    
    # Configure logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Starting AyurVignana API server...")
    print(f"API will be available at: http://localhost:5000/api")
    print(f"Health check endpoint: http://localhost:5000/api/health")
    
    # Run the app
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True,
        threaded=True
    )