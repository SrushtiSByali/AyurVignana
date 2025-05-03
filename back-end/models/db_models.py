"""
MongoDB schema definitions using PyMongo.
Since PyMongo doesn't have a strict schema enforcement like Mongoose,
these are just sample documents that will be inserted.
"""

# Sample herb document schema
herb_schema = {
    "name": "Ashwagandha",  # Herb name (must match prediction output)
    "scientific_name": "Withania somnifera",  # Scientific name
    "nature": "Warming",  # Nature property (Warming, Cooling, Neutral)
    "dosha_compatibility": "Vata, Kapha",  # Which doshas it balances
    "description": "Known as 'Indian Ginseng', Ashwagandha is a powerful adaptogen...",
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
}

# Sample recommendation document schema
recommendation_schema = {
    "symptom": "headache",  # Main symptom (lowercase for easy matching)
    "related_terms": ["migraine", "tension headache", "head pain"],  # Related terms for better matching
    "herbs": [
        {
            "name": "Brahmi",
            "dosage": "1-2 tsp daily",
            "description": "Relieves tension and stress-related headaches...",
            "type": "primary"  # primary or secondary recommendation
        },
        {
            "name": "Jatamansi",
            "dosage": "250-500mg twice daily",
            "description": "Helps calm the nervous system and relieve migraine headaches...",
            "type": "primary"
        }
    ]
}