from pymongo import MongoClient
import sys
import json
from pprint import pprint

# Sample data
herbs = [
    {
        "name": "Ashwagandha",
        "scientific_name": "Withania somnifera",
        "nature": "Warming",
        "dosha_compatibility": "Vata, Kapha",
        "description": "Known as 'Indian Ginseng', Ashwagandha is a powerful adaptogen that helps reduce stress and anxiety while boosting immunity and energy levels. It's particularly effective for addressing nervous exhaustion and insomnia."
    },
    {
        "name": "Tulsi",
        "scientific_name": "Ocimum sanctum",
        "nature": "Cooling",
        "dosha_compatibility": "Vata, Kapha",
        "description": "Sacred Holy Basil is an adaptogenic herb revered in Ayurveda for its healing properties. It helps the body cope with stress and promotes respiratory health, while purifying the blood and supporting the immune system."
    },
    {
        "name": "Turmeric",
        "scientific_name": "Curcuma longa",
        "nature": "Warming",
        "dosha_compatibility": "Vata, Kapha",
        "description": "A powerful anti-inflammatory herb containing curcumin that helps with digestive issues, joint pain, skin conditions, and blood purification. It's a cornerstone of Ayurvedic medicine for treating inflammation."
    }
]

recommendations = [
    {
        "symptom": "headache",
        "related_terms": ["migraine", "tension headache", "head pain"],
        "herbs": [
            {
                "name": "Brahmi",
                "dosage": "1-2 tsp daily",
                "description": "Relieves tension and stress-related headaches while improving mental clarity and focus.",
                "type": "primary"
            },
            {
                "name": "Tulsi",
                "dosage": "1-2 tsp as tea",
                "description": "Supports circulation and can help relieve mild headaches, especially those related to sinus congestion.",
                "type": "secondary"
            }
        ]
    },
    {
        "symptom": "stress",
        "related_terms": ["anxiety", "tension", "nervous", "overwhelm", "worry"],
        "herbs": [
            {
                "name": "Ashwagandha",
                "dosage": "300-500mg twice daily",
                "description": "Reduces cortisol levels and helps the body adapt to stress while supporting adrenal function and energy levels.",
                "type": "primary"
            },
            {
                "name": "Brahmi",
                "dosage": "300mg twice daily",
                "description": "Calms the mind and nervous system while improving cognitive function and memory during stressful periods.",
                "type": "primary"
            }
        ]
    }
]

def setup_mongodb():
    """Setup MongoDB with initial data for AyurVignana"""
    print("Setting up MongoDB for AyurVignana...")
    
    # Connect to MongoDB
    try:
        client = MongoClient("mongodb://localhost:27017/")
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        print("   Is MongoDB installed and running?")
        sys.exit(1)
    
    # Create or get the database
    db = client["ayurvignana"]
    
    # Clear existing collections
    db.herbs.drop()
    db.recommendations.drop()
    print("Cleared existing collections")
    
    # Insert sample data
    try:
        db.herbs.insert_many(herbs)
        db.recommendations.insert_many(recommendations)
        print(f"✅ Inserted {len(herbs)} herbs and {len(recommendations)} recommendation sets")
    except Exception as e:
        print(f"❌ Failed to insert data: {str(e)}")
        sys.exit(1)
    
    # Verify the data
    print("\nVerifying inserted data:")
    
    herb_count = db.herbs.count_documents({})
    recommendation_count = db.recommendations.count_documents({})
    
    print(f"Herbs collection: {herb_count} documents")
    print(f"Recommendations collection: {recommendation_count} documents")
    
    # Print a sample herb
    print("\nSample herb document:")
    sample_herb = db.herbs.find_one()
    if sample_herb:
        pprint(sample_herb)
        print("\nMongoDB setup completed successfully!")
    else:
        print("❌ No herb documents found in the database")

if __name__ == "__main__":
    setup_mongodb()