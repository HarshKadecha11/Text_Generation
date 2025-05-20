
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const generationForm = document.getElementById('generation-form');
    const promptInput = document.getElementById('prompt');
    const modelTypeSelect = document.getElementById('model-type');
    const textLengthInput = document.getElementById('text-length');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.getElementById('btn-text');
    const spinner = document.getElementById('spinner');
    const resultContainer = document.getElementById('result-container');
    const generatedTextElement = document.getElementById('generated-text');

    // Add event listener for form submission
    generationForm.addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // Get user inputs
        const prompt = promptInput.value.trim();
        const modelType = modelTypeSelect.value;
        const textLength = parseInt(textLengthInput.value);
        
        // Validate input
        if (prompt === '') {
            showError('Please enter a prompt');
            return;
        }
        
        if (textLength < 50 || textLength > 500) {
            showError('Text length must be between 50 and 500 characters');
            return;
        }
        
        // Show loading state
        setLoadingState(true);
        
        // Prepare data for API request
        const requestData = {
            prompt: prompt,
            model_type: modelType,
            length: textLength
        };
        
        console.log('Sending request with data:', requestData);
        
        // Send API request to generate text
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                // Convert the response to text first for debugging
                return response.text().then(text => {
                    console.error('Error response body:', text);
                    throw new Error(`Server returned ${response.status}: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);
            // Display the generated text
            if (data.error) {
                showError(data.error);
            } else {
                displayGeneratedText(data.generated_text);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            showError('Error generating text: ' + error.message);
        })
        .finally(() => {
            // Reset loading state
            setLoadingState(false);
        });
    });
    
    // Function to display generated text with typing animation
    function displayGeneratedText(text) {
        // Show the result container
        resultContainer.classList.remove('d-none');
        
        // Scroll to the result container
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // Display the text with typing animation
        generatedTextElement.textContent = '';
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                generatedTextElement.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 10); // typing speed
            }
        }
        
        typeWriter();
    }
    
    // Function to show error message
    function showError(message) {
        console.error('Error:', message);
        
        // Create alert element
        const alertElement = document.createElement('div');
        alertElement.className = 'alert alert-danger alert-dismissible fade show mt-3';
        alertElement.role = 'alert';
        alertElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Insert the alert before the form
        generationForm.parentNode.insertBefore(alertElement, generationForm);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertElement.classList.remove('show');
            setTimeout(() => alertElement.remove(), 300);
        }, 5000);
    }
    
    // Function to toggle loading state
    function setLoadingState(isLoading) {
        if (isLoading) {
            btnText.textContent = 'Generating...';
            spinner.classList.remove('d-none');
            generateBtn.disabled = true;
        } else {
            btnText.textContent = 'Generate Text';
            spinner.classList.add('d-none');
            generateBtn.disabled = false;
        }
    }
});