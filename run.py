# !/usr/bin/env python

import os
import sys

# Ensure the current directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import after path setup
from app import app

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    print("Starting Flask server on http://0.0.0.0:5001")
    print("Press Ctrl+C to quit")

    # Run the Flask application
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), debug=True)