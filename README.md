# 🧠 TextGenius AI

> Unleash the power of neural networks to generate human-like content on demand

![Python](https://img.shields.io/badge/python-3.9-blue)
![Flask](https://img.shields.io/badge/flask-2.0+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Overview

TextGenius AI is a sophisticated web application that leverages advanced neural network architectures to generate coherent, contextually-relevant text based on user prompts. Whether you need creative writing inspiration, content ideas, or just want to explore the capabilities of modern AI text generation, TextGenius has you covered.

## 🚀 Features

- **Dual AI Models**: Choose between two powerful neural networks:
  - **LSTM Model**: Excellent for structured, coherent paragraph generation
  - **GPT-like Model**: Advanced semantic understanding with topic awareness
  
- **Interactive Web Interface**: Clean, responsive UI for seamless interaction with the AI

- **Customization Options**:
  - Adjust output length to fit your needs
  - Topic-specific generation for targeted content
  - Real-time text generation with minimal latency

- **Topic Intelligence**: The system recognizes specialized topics and categories to generate more relevant content

## 📋 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/textgenius-ai.git
   cd textgenius-ai
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the web interface**
   - Open your browser and navigate to: http://localhost:5001


## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/about` | GET | About page with project information |
| `/topics` | GET | Returns available specialized topics |
| `/generate` | POST | Generate text based on prompt |
| `/health` | GET | Simple health check endpoint |

## 💡 Use Cases

- **Content Creation**: Generate blog post drafts, creative writing prompts, or marketing copy
- **Education**: Aid in learning how neural networks process and generate language
- **Research**: Experiment with different prompts to understand AI text capabilities and limitations
- **Brainstorming**: Overcome writer's block by generating new ideas around a topic

## 🛠️ Advanced Configuration

TextGenius AI can be customized beyond the default settings:

- Modify port settings in `run.py`
- Adjust model parameters in the respective model files
- Extend the topic database by adding to the categories in the GPT model

## 🤝 Contributing

Contributions are welcome! If you'd like to improve TextGenius AI:

1. Fork the repository
2. Create a feature branch (`git checkout -b amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Enhancements

- Fine-tuning capabilities for domain-specific text generation
- Multi-language support
- Text-to-speech integration for generated content
- API keys for programmatic access
- User accounts to save favorite prompts and generations

---
