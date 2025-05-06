document.addEventListener('DOMContentLoaded', function() {
    // API URL - Change this to your actual API URL
    const API_URL = 'http://localhost:5000/api';
    
    // Add a console log to check configuration
    console.log('Connecting to API at:', API_URL);
    
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
    const resultImage = document.getElementById('result-image');
    
    const symptomsInput = document.getElementById('symptoms');
    const recommendBtn = document.getElementById('recommend-btn');
    const recommendationLoading = document.getElementById('recommendation-loading');
    const recommendationProgress = document.getElementById('recommendation-progress');
    const recommendationsContainer = document.getElementById('recommendations-container');
    const recommendationsList = document.getElementById('recommendations-list');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');
    const recommendationPills = document.querySelectorAll('.recommendation-pill');
    
    // For animation fallback
    function gsapFallback(element) {
        element.style.opacity = '0';
        element.style.display = 'block';
        let opacity = 0;
        const fadeIn = setInterval(() => {
            opacity += 0.1;
            element.style.opacity = opacity;
            if (opacity >= 1) clearInterval(fadeIn);
        }, 30);
    }
    
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
        
        // Simulate initial progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += 2;
            if (progress > 90) clearInterval(interval); // Stop at 90% and wait for real response
            recognitionProgress.style.width = `${progress}%`;
        }, 100);
        
        // Prepare form data
        const formData = new FormData();
        formData.append('image', herbImageInput.files[0]);
        
        console.log('Sending request to:', `${API_URL}/predict`);
        
        // Make API call
        fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Received response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);
            // Stop progress animation
            clearInterval(interval);
            recognitionProgress.style.width = '100%';
            
            // Hide loading after small delay
            setTimeout(() => {
                recognitionLoading.style.display = 'none';
                
                // Update result data
                herbName.textContent = data.name;
                scientificName.textContent = data.scientific;
                herbNature.textContent = data.nature;
                herbDosha.textContent = data.dosha;
                herbDescription.textContent = data.description;
                
                // Convert confidence to number if it's a string
                const confidence = typeof data.confidence === 'string' 
                    ? parseFloat(data.confidence) 
                    : data.confidence;
                    
                confidenceScore.textContent = `${confidence.toFixed(1)}%`;
                confidenceMeter.style.width = `${confidence}%`;
                
                // Update the result image if provided
                if (data.image_url) {
                    resultImage.src = data.image_url;
                }
                
                // Set the accuracy badge
                if (confidence >= 90) {
                    accuracyBadge.textContent = 'High Accuracy';
                    accuracyBadge.style.backgroundColor = '#4caf50';
                } else if (confidence >= 80) {
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
        })
        .catch(error => {
            console.error('Error:', error);
            clearInterval(interval);
            
            // Display error message with more details
            recognitionLoading.style.display = 'none';
            alert(`Error identifying herb: ${error.message}`);
        });
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
        const symptoms = symptomsInput.value.trim();

        if (!symptoms) {
            alert('Please describe your symptoms first!');
            return;
        }

        // Show loading
        recommendationLoading.style.display = 'block';
        recommendationsContainer.style.display = 'none';

        // Simulate initial progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += 2;
            if (progress > 90) clearInterval(interval); // Stop at 90% and wait for real response
            recommendationProgress.style.width = `${progress}%`;
        }, 100);
        
        console.log('Sending recommendation request for symptoms:', symptoms);
        
        // Make API call
        fetch(`${API_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symptoms: symptoms })
        })
        .then(response => {
            console.log('Received recommendation response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received recommendation data:', data);
            // Stop progress animation
            clearInterval(interval);
            recommendationProgress.style.width = '100%';
            
            // Hide loading after small delay
            setTimeout(() => {
                recommendationLoading.style.display = 'none';
                
                // Show recommendations
                recommendationsContainer.style.display = 'block';
                
                // Clear previous recommendations
                recommendationsList.innerHTML = '';
                
                // Display recommendations
                if (data.recommendations && data.recommendations.length > 0) {
                    data.recommendations.forEach((recommendation) => {
                        const card = document.createElement('div');
                        card.className = 'recommendation-card';
                        card.setAttribute('data-type', recommendation.type);
                        
                        card.innerHTML = `
                            <h5>${recommendation.name} <span class="dosage">${recommendation.dosage}</span></h5>
                            <p>${recommendation.description}</p>
                        `;
                        
                        recommendationsList.appendChild(card);
                    });
                    
                    // Show all by default
                    document.querySelector('.recommendation-pill[data-filter="all"]').click();
                } else {
                    recommendationsList.innerHTML = '<p>No recommendations found for the given symptoms.</p>';
                }
                
                // Animate entrance
                gsapFallback(recommendationsContainer);
            }, 500);
        })
        .catch(error => {
            console.error('Error with recommendations:', error);
            clearInterval(interval);
            
            // Display error message with more details
            recommendationLoading.style.display = 'none';
            alert(`Error getting recommendations: ${error.message}`);
        });
    });
    
    // Check API health on page load
    fetch(`${API_URL}/health`)
        .then(response => {
            console.log('Health check status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('API Status:', data.status);
        })
        .catch(error => {
            console.error('API Health Check Failed:', error);
            console.warn('Backend server might not be running. Please start the Flask server on port 5000.');
        });
});