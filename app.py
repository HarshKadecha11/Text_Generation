from flask import Flask, render_template, request, jsonify
import os
import sys
import traceback

# Make sure models are in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Initialize Flask app
app = Flask(__name__)

# Ensure NLTK data directory exists
os.makedirs(os.path.join(os.path.expanduser('~'), 'nltk_data'), exist_ok=True)

# Pre-download NLTK resources before initializing models
import nltk

nltk.download('punkt', quiet=False)

# Global variables for models
lstm_model = None
gpt_model = None


# Initialize models
def initialize_models():
    global lstm_model, gpt_model
    try:
        from models.lstm_model import LSTMTextGenerator
        from models.gpt_model import SimpleGPTModel

        print("Initializing LSTM model...")
        lstm_model = LSTMTextGenerator()
        print("Initializing GPT model...")
        gpt_model = SimpleGPTModel()
        print("Models initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing models: {str(e)}")
        traceback.print_exc()
        return False


# Try to initialize models
initialize_models()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')


@app.route('/topics')
def get_topics():
    """Return the list of specialized topics available in the model"""
    global gpt_model

    # Check if model is initialized
    if gpt_model is None:
        if not initialize_models():
            return jsonify({'error': 'Models could not be initialized.'}), 500

    # Get the specific topics from the model
    specific_topics = {}
    if hasattr(gpt_model, 'specific_topics'):
        for topic, data in gpt_model.specific_topics.items():
            specific_topics[topic] = data.get('description', f"Information about {topic}")

    # Get categories and their keywords
    categories = {}
    if hasattr(gpt_model, 'categories'):
        for category, data in gpt_model.categories.items():
            # Include only a selection of the most representative keywords
            categories[category] = data.get('keywords', [])[:10]  # limit to 10 keywords

    return jsonify({
        'specific_topics': specific_topics,
        'categories': categories
    })


@app.route('/generate', methods=['POST'])
def generate_text():
    """Generate text based on user input"""
    global lstm_model, gpt_model

    try:
        # Check if models are initialized
        if lstm_model is None or gpt_model is None:
            # Attempt to initialize the models again
            if not initialize_models():
                return jsonify({'error': 'Text generation models could not be initialized.'}), 500

        # Parse the request data
        data = request.get_json()

        if not data:
            print("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400

        prompt = data.get('prompt', '')
        model_type = data.get('model_type', 'lstm')
        try:
            length = int(data.get('length', 200))
        except (ValueError, TypeError):
            length = 200

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Fallback text generation that doesn't depend on models
        def generate_fallback_text(prompt, length):
            return f"The topic of {prompt} is interesting and has many aspects worth exploring. It continues to evolve and offers valuable insights across different contexts. When examining {prompt}, it's important to consider various perspectives and implications. Further research on {prompt} may reveal new insights and applications."[
                   :length]

        # Generate text using the appropriate model with error handling
        try:
            if model_type.lower() == 'lstm':
                generated_text = lstm_model.generate(prompt, length)
            else:
                generated_text = gpt_model.generate(prompt, length)

            # If generation failed or returned empty text, use fallback
            if not generated_text or len(generated_text.strip()) < 10:
                generated_text = generate_fallback_text(prompt, length)
        except Exception as e:
            print(f"Error in model text generation: {str(e)}")
            traceback.print_exc()
            generated_text = generate_fallback_text(prompt, length)

        # Ensure text contains the prompt (for relevance)
        if not any(word.lower() in generated_text.lower() for word in prompt.lower().split() if len(word) > 3):
            prefix = f"Regarding {prompt}: "
            # Make sure we don't exceed the requested length
            if len(prefix) + len(generated_text) > length:
                generated_text = prefix + generated_text[:length - len(prefix)]
            else:
                generated_text = prefix + generated_text

        # Return the generated text
        return jsonify({'generated_text': generated_text})

    except Exception as e:
        # Log the full exception
        print(f"Error in generate_text: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'Error generating text: {str(e)}'}), 500


# Simple health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    # Run the app
    print("Starting Flask application...")
    app.run(debug=True)