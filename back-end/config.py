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
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'back-end\AyurVignana_prediction_cnn_.h5')
    IMG_SIZE = (224, 224)  # Input size expected by the model
    
    # Classes the model was trained on (update with your actual classes)
    CLASSES = [
    'Ajwain seed', 'Aloevera leaf', 'Aloevera plant', 'Amla', 'Amla leaf', 'Amla plant',
    'Amrutaballi', 'Amruthaballi leaf', 'Arali leaf', 'Ashoka leaf', 'Ashoka plant',
    'Ashwagandha plant', 'Astma_weed', 'Bael fruit', 'Bakuchi seed', 'Bamboo plant',
    'Banana', 'Ber', 'Betel leaf', 'Betel Nut plant', 'Bhrami leaf', 'Bhrami plant',
    'Bitter gourd', 'Bringaraja leaf', 'Cardamom', 'Castor leaf', 'Castor plant',
    'Catharanthus leaf', 'Chrysanthemum', 'Clove', 'Coconut', 'Coriander leaf',
    'Coriander seed', 'Curry leaf', 'Curry_Leaf plant', 'Doddapatre plant',
    'Doddapatre leaf', 'Drumstick leaf', 'Ekka leaf', 'Eucalyptus leaf', 'Fennel seed',
    'Fenugreek seed', 'Fig', 'Garlic', 'Gasagase leaf', 'Geranium plant', 'Ginger',
    'Ginger leaf', 'Globe Amaranth', 'Gotu Kola leaf', 'Grapes', 'Henna leaf',
    'Henna plant', 'Hibiscus leaf', 'Hibiscus plant', 'Honge leaf', 'Honge plant',
    'Insulin plant', 'Jackfruit', 'Jamun', 'Jasmine leaf', 'Jasmine plant', 'Jeera seed',
    'Kadamba', 'kamakasturi leaf', 'Kasambruga leaf', 'Kokum', 'Kutki', 'Lantana leaf',
    'Lemon', 'Lemon leaf', 'Lemon plant', 'Lemongrass leaf', 'Malabar_Nut leaf',
    'Mango leaf', 'Mango plant', 'Mint leaf', 'Mint plant', 'Mustard seed',
    'Nagadali plant', 'Neem leaf', 'Neem plant', 'Nithyapushpa plant', 'Noni',
    'Noni plant', 'Nooni leaf', 'Padri leaf', 'Palak(Spinach) leaf', 'Papaya',
    'Papaya leaf', 'Papaya plant', 'Parijatha leaf', 'Pepper plant', 'Pepper seed',
    'Pomegranate', 'Pomegranate plant', 'Psyllium seed', 'Raktachandini plant',
    'Rose apple', 'Rose leaf', 'Rose plant', 'Saffron', 'Sampige leaf', 'Sesame seed',
    'Tamarind leaf', 'Tamarind', 'Taro leaf', 'Tecoma leaf', 'Tendu fruit',
    'Thumbe leaf', 'Tomato leaf', 'Tulsi leaf', 'Tulsi plant', 'Turmeric',
    'Turmeric leaf', 'White musalli', 'Wood_sorel plant'
]
