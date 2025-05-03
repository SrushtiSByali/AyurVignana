import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ayurvignana-secret-key')
    DEBUG = True
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'ayurvignana')
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    
    # Model Configuration
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AyurVignana_prediction_cnn.h5')
    IMG_SIZE = (224, 224)  # Input size expected by the model
    
    # Classes the model was trained on (update with your actual classes)
    CLASSES = [
        'Ashwagandha', 'Tulsi', 'Turmeric', 'Brahmi', 'Neem', 'Shatavari',
        # Add all other herb classes your model was trained on
    ]