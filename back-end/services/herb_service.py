"""
Service for herb data operations with MongoDB
"""
import re

def get_herb_by_name(db, herb_name):
    """
    Get herb details from the database by name
    
    Args:
        db: MongoDB database connection
        herb_name: Name of the herb to search for
        
    Returns:
        dict: Herb details or None if not found
    """
    # Case-insensitive search for herb name
    herb = db.herbs.find_one({"name": {"$regex": f"^{re.escape(herb_name)}$", "$options": "i"}})
    return herb

def get_recommendations_by_symptoms(db, symptoms_text):
    """
    Get herb recommendations based on user symptoms
    
    Args:
        db: MongoDB database connection
        symptoms_text: Text containing user symptoms
        
    Returns:
        list: List of recommended herbs for the symptoms
    """
    symptoms_text = symptoms_text.lower()
    recommendations = []
    
    # Search for each symptom in the database
    all_recommendations = db.recommendations.find({})
    
    for rec in all_recommendations:
        # Check if the symptom or any related terms match
        symptom_matches = rec["symptom"] in symptoms_text
        related_terms_match = any(term in symptoms_text for term in rec.get("related_terms", []))
        
        if symptom_matches or related_terms_match:
            # Add herbs from this recommendation to the results
            for herb in rec["herbs"]:
                # Check if this herb is already in recommendations
                existing = next((r for r in recommendations if r["name"] == herb["name"]), None)
                if not existing:
                    recommendations.append(herb)
    
    return recommendations

def seed_database(db):
    """
    Seed the database with initial herb and recommendation data
    
    Args:
        db: MongoDB database connection
    """
    # First check if data already exists
    if db.herbs.count_documents({}) > 0:
        print("Database already seeded, skipping...")
        return
    
    # Seed herbs collection
    herbs = [
        {
            "name": "Ashwagandha",
            "scientific_name": "Withania somnifera",
            "nature": "Warming",
            "dosha_compatibility": "Vata, Kapha",
            "description": "Known as 'Indian Ginseng', Ashwagandha is a powerful adaptogen that helps reduce stress and anxiety while boosting immunity and energy levels. It's particularly effective for addressing nervous exhaustion and insomnia.",
            "properties": {
                "taste": ["Bitter", "Astringent"],
                "potency": "Hot",
                "post_digestive": "Sweet"
            },
            "benefits": [
                "Reduces stress and anxiety",
                "Boosts immunity",
                "Improves energy levels",
                "Helps with insomnia"
            ],
            "usage": {
                "dosage": "1-2 teaspoons of powder daily",
                "method": "Mix with warm milk or water",
                "timing": "Best taken before bed"
            },
            "contraindications": [
                "Pregnancy",
                "Severe autoimmune conditions"
            ]
        },
        {
            "name": "Tulsi",
            "scientific_name": "Ocimum sanctum",
            "nature": "Cooling",
            "dosha_compatibility": "Vata, Kapha",
            "description": "Sacred Holy Basil is an adaptogenic herb revered in Ayurveda for its healing properties. It helps the body cope with stress and promotes respiratory health, while purifying the blood and supporting the immune system.",
            "properties": {
                "taste": ["Pungent", "Bitter"],
                "potency": "Hot",
                "post_digestive": "Pungent"
            },
            "benefits": [
                "Respiratory health",
                "Blood purification",
                "Immune support",
                "Stress management"
            ],
            "usage": {
                "dosage": "1-2 teaspoons of dried herb",
                "method": "As tea or eaten raw",
                "timing": "Throughout the day"
            },
            "contraindications": [
                "May reduce fertility",
                "Blood thinning medications"
            ]
        },
        {
            "name": "Turmeric",
            "scientific_name": "Curcuma longa",
            "nature": "Warming",
            "dosha_compatibility": "Vata, Kapha",
            "description": "A powerful anti-inflammatory herb containing curcumin that helps with digestive issues, joint pain, skin conditions, and blood purification. It's a cornerstone of Ayurvedic medicine for treating inflammation.",
            "properties": {
                "taste": ["Bitter", "Pungent", "Astringent"],
                "potency": "Hot",
                "post_digestive": "Pungent"
            },
            "benefits": [
                "Anti-inflammatory",
                "Blood purification",
                "Digestive support",
                "Joint health"
            ],
            "usage": {
                "dosage": "1/2 to 1 teaspoon daily",
                "method": "Mix with warm milk or in food",
                "timing": "With meals"
            },
            "contraindications": [
                "Gallbladder problems",
                "Blood thinning medications",
                "Before surgery"
            ]
        },
        {
            "name": "Brahmi",
            "scientific_name": "Bacopa monnieri",
            "nature": "Cooling",
            "dosha_compatibility": "Pitta, Vata",
            "description": "Enhances cognitive function, improves memory, and helps manage anxiety and stress. Traditionally used to support the nervous system and improve concentration, it's considered one of the best brain tonics in Ayurveda.",
            "properties": {
                "taste": ["Bitter", "Sweet", "Astringent"],
                "potency": "Cold",
                "post_digestive": "Sweet"
            },
            "benefits": [
                "Cognitive enhancement",
                "Memory improvement",
                "Anxiety reduction",
                "Nervous system support"
            ],
            "usage": {
                "dosage": "300-600mg daily",
                "method": "As capsules or with ghee",
                "timing": "Morning and evening"
            },
            "contraindications": [
                "May slow heart rate",
                "Excess can cause digestive upset"
            ]
        },
        {
            "name": "Shatavari",
            "scientific_name": "Asparagus racemosus",
            "nature": "Cooling",
            "dosha_compatibility": "Pitta, Vata",
            "description": "Known as the 'Queen of Herbs', Shatavari is primarily used for female reproductive health. It helps balance hormones, supports lactation, and strengthens the immune system. It's also beneficial for digestive health.",
            "properties": {
                "taste": ["Sweet", "Bitter"],
                "potency": "Cold",
                "post_digestive": "Sweet"
            },
            "benefits": [
                "Female reproductive health",
                "Hormonal balance",
                "Lactation support",
                "Digestive health"
            ],
            "usage": {
                "dosage": "1-2 teaspoons daily",
                "method": "Mix with warm milk or water",
                "timing": "Morning and evening"
            },
            "contraindications": [
                "Edema",
                "Excess kapha conditions"
            ]
        },
        {
            "name": "Neem",
            "scientific_name": "Azadirachta indica",
            "nature": "Cooling",
            "dosha_compatibility": "Pitta, Kapha",
            "description": "A powerful detoxifying herb with antibacterial, antifungal, and blood-purifying properties. Neem is used for skin conditions, dental health, and to support the liver. It's also an effective immune booster.",
            "properties": {
                "taste": ["Bitter"],
                "potency": "Cold",
                "post_digestive": "Pungent"
            },
            "benefits": [
                "Blood purification",
                "Skin health",
                "Dental hygiene",
                "Liver support"
            ],
            "usage": {
                "dosage": "250-500mg twice daily",
                "method": "As capsules or tea",
                "timing": "Before meals"
            },
            "contraindications": [
                "Pregnancy",
                "Trying to conceive",
                "Excessive for Vata types"
            ]
        }
    ]
    
    # Insert herbs
    db.herbs.insert_many(herbs)
    print(f"Inserted {len(herbs)} herbs into the database")
    
    # Seed recommendations collection
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
                    "name": "Jatamansi",
                    "dosage": "250-500mg twice daily",
                    "description": "Helps calm the nervous system and relieve migraine headaches by reducing vascular inflammation.",
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
            "symptom": "joint pain",
            "related_terms": ["arthritis", "inflammation", "stiff joints"],
            "herbs": [
                {
                    "name": "Turmeric",
                    "dosage": "1 tsp with warm milk",
                    "description": "Reduces inflammation and relieves joint pain and stiffness through its active compound curcumin.",
                    "type": "primary"
                },
                {
                    "name": "Ashwagandha",
                    "dosage": "500mg twice daily",
                    "description": "Helps reduce inflammation and strengthen the immune system while providing adrenal support.",
                    "type": "secondary"
                },
                {
                    "name": "Neem",
                    "dosage": "250-500mg daily",
                    "description": "Helps purify the blood and reduce inflammation associated with arthritis and autoimmune conditions.",
                    "type": "secondary"
                }
            ]
        },
        {
            "symptom": "digestive",
            "related_terms": ["indigestion", "bloating", "gas", "stomach", "constipation", "digestion"],
            "herbs": [
                {
                    "name": "Tulsi",
                    "dosage": "1-2 tsp as tea",
                    "description": "Supports healthy digestion and can help relieve gas, bloating, and mild digestive discomfort.",
                    "type": "primary"
                },
                {
                    "name": "Turmeric",
                    "dosage": "1/2 tsp with warm water",
                    "description": "Reduces inflammation in the digestive tract and supports healthy digestion and nutrient absorption.",
                    "type": "primary"
                },
                {
                    "name": "Neem",
                    "dosage": "250mg before meals",
                    "description": "Helps cleanse the digestive tract and supports healthy intestinal flora.",
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
                },
                {
                    "name": "Tulsi",
                    "dosage": "1-2 tsp of dried herb as tea",
                    "description": "Calms the mind and supports adrenal function during stressful periods, while boosting mental clarity.",
                    "type": "secondary"
                }
            ]
        },
        {
            "symptom": "skin",
            "related_terms": ["acne", "eczema", "rash", "psoriasis", "dermatitis", "skin problems"],
            "herbs": [
                {
                    "name": "Neem",
                    "dosage": "500mg twice daily",
                    "description": "Purifies the blood and has antibacterial properties that help clear acne and skin infections.",
                    "type": "primary"
                },
                {
                    "name": "Turmeric",
                    "dosage": "External paste application",
                    "description": "Applied externally, helps reduce inflammation and fight bacteria while accelerating healing.",
                    "type": "primary"
                },
                {
                    "name": "Brahmi",
                    "dosage": "300mg daily",
                    "description": "Helps cool the skin and reduce pitta-related skin conditions like inflammation and redness.",
                    "type": "secondary"
                }
            ]
        }
    ]
    
    # Insert recommendations
    db.recommendations.insert_many(recommendations)
    print(f"Inserted {len(recommendations)} recommendation sets into the database")