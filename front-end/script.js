document.addEventListener('DOMContentLoaded', function() {
    // Variables
    const herbImageInput = document.getElementById('herb-image');
    const imagePreview = document.getElementById('image-preview');
    const previewContainer = document.getElementById('preview-container');
    const identifyBtn = document.getElementById('identify-btn');
    const recognitionLoading = document.getElementById('recognition-loading');
    const recognitionProgress = document.getElementById('recognition-progress');
    const recognitionResult = document.getElementById('recognition-result');
    const herbName = document.getElementById('herb-name');
    const scientificName = document.getElementById('scientific-name');
    const herbNature = document.getElementById('herb-nature');
    const herbDosha = document.getElementById('herb-dosha');
    const herbDescription = document.getElementById('herb-description');
    const confidenceScore = document.getElementById('confidence-score');
    const confidenceMeter = document.getElementById('confidence-meter');
    const accuracyBadge = document.getElementById('accuracy-badge');
    
    const symptomsInput = document.getElementById('symptoms');
    const recommendBtn = document.getElementById('recommend-btn');
    const recommendationLoading = document.getElementById('recommendation-loading');
    const recommendationProgress = document.getElementById('recommendation-progress');
    const recommendationsContainer = document.getElementById('recommendations-container');
    const recommendationsList = document.getElementById('recommendations-list');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');
    const recommendationPills = document.querySelectorAll('.recommendation-pill');
    
    // Sample herb data (this would come from your model in production)
    const sampleHerbs = [
        {
            name: "Ashwagandha",
            scientific: "Withania somnifera",
            nature: "Warming",
            dosha: "Vata, Kapha",
            description: "Known as 'Indian Ginseng', Ashwagandha is a powerful adaptogen that helps reduce stress and anxiety while boosting immunity and energy levels. It's particularly effective for addressing nervous exhaustion and insomnia.",
            confidence: 93
        },
        {
            name: "Tulsi",
            scientific: "Ocimum sanctum",
            nature: "Cooling",
            dosha: "Vata, Kapha",
            description: "Sacred Holy Basil is an adaptogenic herb revered in Ayurveda for its healing properties. It helps the body cope with stress and promotes respiratory health, while purifying the blood and supporting the immune system.",
            confidence: 89
        },
        {
            name: "Turmeric",
            scientific: "Curcuma longa",
            nature: "Warming",
            dosha: "Vata, Kapha",
            description: "A powerful anti-inflammatory herb containing curcumin that helps with digestive issues, joint pain, skin conditions, and blood purification. It's a cornerstone of Ayurvedic medicine for treating inflammation.",
            confidence: 95
        },
        {
            name: "Brahmi",
            scientific: "Bacopa monnieri",
            nature: "Cooling",
            dosha: "Pitta, Vata",
            description: "Enhances cognitive function, improves memory, and helps manage anxiety and stress. Traditionally used to support the nervous system and improve concentration, it's considered one of the best brain tonics in Ayurveda.",
            confidence: 91
        },
        {
            name: "Shatavari",
            scientific: "Asparagus racemosus",
            nature: "Cooling",
            dosha: "Pitta, Vata",
            description: "Known as the 'Queen of Herbs', Shatavari is primarily used for female reproductive health. It helps balance hormones, supports lactation, and strengthens the immune system. It's also beneficial for digestive health.",
            confidence: 88
        },
        {
            name: "Neem",
            scientific: "Azadirachta indica",
            nature: "Cooling",
            dosha: "Pitta, Kapha",
            description: "A powerful detoxifying herb with antibacterial, antifungal, and blood-purifying properties. Neem is used for skin conditions, dental health, and to support the liver. It's also an effective immune booster.",
            confidence: 94
        }
    ];
    
    // Sample recommendations data (this would come from your database in production)
    const sampleRecommendations = {
        "headache": [
            {
                name: "Brahmi",
                dosage: "1-2 tsp daily",
                description: "Relieves tension and stress-related headaches while improving mental clarity and focus.",
                type: "primary"
            },
            {
                name: "Jatamansi",
                dosage: "250-500mg twice daily",
                description: "Helps calm the nervous system and relieve migraine headaches by reducing vascular inflammation.",
                type: "primary"
            },
            {
                name: "Shankhpushpi",
                dosage: "1-2 tsp with warm milk",
                description: "Supports cerebral circulation and relieves headaches caused by mental fatigue.",
                type: "secondary"
            }
        ],
        "joint pain": [
            {
                name: "Turmeric",
                dosage: "1 tsp with warm milk",
                description: "Reduces inflammation and relieves joint pain and stiffness through its active compound curcumin.",
                type: "primary"
            },
            {
                name: "Boswellia",
                dosage: "300-400mg three times daily",
                description: "Alleviates pain and improves mobility in arthritic conditions by inhibiting inflammatory enzymes.",
                type: "primary"
            },
            {
                name: "Nirgundi",
                dosage: "External application as oil",
                description: "Provides localized pain relief and reduces swelling when applied directly to affected joints.",
                type: "secondary"
            }
        ],
        "digestive": [
            {
                name: "Ginger",
                dosage: "1-2g daily",
                description: "Relieves indigestion, bloating, and nausea while improving digestive fire (agni) and nutrient absorption.",
                type: "primary"
            },
            {
                name: "Triphala",
                dosage: "500mg twice daily",
                description: "Supports regular bowel movements, detoxifies the GI tract, and balances all three doshas for optimal digestive health.",
                type: "primary"
            },
            {
                name: "Fennel",
                dosage: "1 tsp seeds after meals",
                description: "Reduces gas, bloating, and acts as a gentle digestive stimulant that's safe for daily use.",
                type: "secondary"
            }
        ],
        "stress": [
            {
                name: "Ashwagandha",
                dosage: "300-500mg twice daily",
                description: "Reduces cortisol levels and helps the body adapt to stress while supporting adrenal function and energy levels.",
                type: "primary"
            },
            {
                name: "Tulsi",
                dosage: "1-2 tsp of dried herb as tea",
                description: "Calms the mind and supports adrenal function during stressful periods, while boosting mental clarity.",
                type: "primary"
            },
            {
                name: "Jatamansi",
                dosage: "250mg twice daily",
                description: "Acts as a natural tranquilizer that soothes the nervous system without causing drowsiness.",
                type: "secondary"
            }
        ],
        "skin": [
            {
                name: "Neem",
                dosage: "500mg twice daily",
                description: "Purifies the blood and has antibacterial properties that help clear acne and skin infections.",
                type: "primary"
            },
            {
                name: "Manjistha",
                dosage: "250-500mg twice daily",
                description: "Detoxifies the blood and lymphatic system, helping to clear up skin conditions from the inside out.",
                type: "primary"
            },
            {
                name: "Turmeric",
                dosage: "External paste application",
                description: "Applied externally, helps reduce inflammation and fight bacteria while accelerating healing.",
                type: "secondary"
            }
        ]
    };
    
    // Handle image preview
    herbImageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            previewContainer.style.display = 'block';
        }
        reader.readAsDataURL(file);
    });
    
    // Handle herb identification
    identifyBtn.addEventListener('click', function() {
        if (!herbImageInput.files[0]) {
            alert('Please select an image first!');
            return;
        }
        
        // Show loading, hide results
        recognitionLoading.style.display = 'block';
        recognitionResult.style.display = 'none';
        
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            recognitionProgress.style.width = `${progress}%`;
            
            if (progress >= 100) {
                clearInterval(interval);
                // Hide loading after 1.5s
                setTimeout(() => {
                    recognitionLoading.style.display = 'none';
                    
                    // Show result with random herb from sample data
                    const randomHerb = sampleHerbs[Math.floor(Math.random() * sampleHerbs.length)];
                    herbName.textContent = randomHerb.name;
                    scientificName.textContent = randomHerb.scientific;
                    herbNature.textContent = randomHerb.nature;
                    herbDosha.textContent = randomHerb.dosha;
                    herbDescription.textContent = randomHerb.description;
                    confidenceScore.textContent = `${randomHerb.confidence}%`;
                    confidenceMeter.style.width = `${randomHerb.confidence}%`;
                    
                    // Set the accuracy badge
                    if (randomHerb.confidence >= 90) {
                        accuracyBadge.textContent = 'High Accuracy';
                        accuracyBadge.style.backgroundColor = '#4caf50';
                    } else if (randomHerb.confidence >= 80) {
                        accuracyBadge.textContent = 'Good Accuracy';
                        accuracyBadge.style.backgroundColor = '#ff9800';
                    } else {
                        accuracyBadge.textContent = 'Moderate Accuracy';
                        accuracyBadge.style.backgroundColor = '#f44336';
                    }
                    
                    recognitionResult.style.display = 'block';
                    
                    // Animate the entrance of results
                    gsapFallback(recognitionResult);
                }, 500);
            }
        }, 100);
    });
    
    // Handle suggestion chips
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', function() {
            const symptom = this.textContent;
            
            // Add the symptom to textarea if not already there
            if (!symptomsInput.value.includes(symptom)) {
                if (symptomsInput.value.trim() !== '') {
                    symptomsInput.value += ', ';
                }
                symptomsInput.value += symptom;
            }
            
            // Focus back on textarea
            symptomsInput.focus();
        });
    });
    
    // Handle recommendation filter pills
    recommendationPills.forEach(pill => {
        pill.addEventListener('click', function() {
            // Update active state
            recommendationPills.forEach(p => p.classList.remove('active'));
            this.classList.add('active');
            
            // Get filter value
            const filter = this.getAttribute('data-filter');
            
            // Apply filter
            const cards = document.querySelectorAll('.recommendation-card');
            cards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-type') === filter) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // Handle herb recommendations
    recommendBtn.addEventListener('click', function () {
        const symptoms = symptomsInput.value.trim().toLowerCase();

        if (!symptoms) {
            alert('Please describe your symptoms first!');
            return;
        }

        // Show loading
        recommendationLoading.style.display = 'block';
        recommendationsContainer.style.display = 'none';

        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            recommendationProgress.style.width = `${progress}%`;

            if (progress >= 100) {
                clearInterval(interval);

                // Hide loading after 1.5s
                setTimeout(() => {
                    recommendationLoading.style.display = 'none';

                    // Show recommendations
                    recommendationsContainer.style.display = 'block';

                    // Clear previous recommendations
                    recommendationsList.innerHTML = '';

                    // Find matching recommendations
                    const matchedRecommendations = [];
                    Object.keys(sampleRecommendations).forEach((key) => {
                        if (symptoms.includes(key)) {
                            matchedRecommendations.push(...sampleRecommendations[key]);
                        }
                    });

                    // Display recommendations
                    if (matchedRecommendations.length > 0) {
                        matchedRecommendations.forEach((recommendation) => {
                            const card = document.createElement('div');
                            card.className = 'recommendation-card';
                            card.setAttribute('data-type', recommendation.type);

                            card.innerHTML = `
                                <h5>${recommendation.name} <span class="dosage">${recommendation.dosage}</span></h5>
                                <p>${recommendation.description}</p>
                            `;

                            recommendationsList.appendChild(card);
                        });
                    } else {
                        recommendationsList.innerHTML = '<p>No recommendations found for the given symptoms.</p>';
                    }
                }, 500);
            }
        }, 100);
    });
});