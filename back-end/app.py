from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from tensorflow.keras.models import load_model
from services.prediction_service import predict_herb
from services.herb_service import get_herb_by_name, get_recommendations_by_symptoms
from utils.image_utils import preprocess_image
from pymongo import MongoClient
from config import Config

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Load configuration
app.config.from_object(Config)

# Connect to MongoDB
client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['MONGO_DB_NAME']]

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the trained model
model = load_model(app.config['MODEL_PATH'])
print("Model loaded successfully")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "AyurVignana API is running"})

@app.route('/api/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint to predict herb from uploaded image"""
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    
    # Save the uploaded image
    filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    try:
        # Preprocess image and predict
        processed_image = preprocess_image(file_path)
        prediction, confidence = predict_herb(model, processed_image)
        
        # Get herb details from database
        herb_details = get_herb_by_name(db, prediction)
        
        if not herb_details:
            return jsonify({
                "error": "Herb details not found in database",
                "prediction": prediction,
                "confidence": confidence
            }), 404
        
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
    data = request.json
    if not data or 'symptoms' not in data:
        return jsonify({"error": "No symptoms provided"}), 400
    
    symptoms = data['symptoms'].lower()
    
    try:
        # Get recommendations from database
        recommendations = get_recommendations_by_symptoms(db, symptoms)
        
        return jsonify({"recommendations": recommendations})
    
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)