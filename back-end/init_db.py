"""
Initialize and seed the MongoDB database with herb data
"""
from pymongo import MongoClient
from config import Config
from services.herb_service import seed_database

def init_database():
    """Initialize and seed the MongoDB database"""
    # Connect to MongoDB
    print(f"Connecting to MongoDB at {Config.MONGO_URI}")
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]
    
    # Seed database with initial data
    print("Seeding database with initial herb and recommendation data")
    seed_database(db)
    
    print(f"Database '{Config.MONGO_DB_NAME}' initialization complete!")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    init_database()