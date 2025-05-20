import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

def clean_text(text):
    """Clean and preprocess text data"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = ''.join(c for c in text if c not in string.punctuation)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_text(text):
    """Tokenize text into words"""
    return word_tokenize(text)
import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

def clean_text(text):
    """Clean and preprocess text data"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = ''.join(c for c in text if c not in string.punctuation)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_text(text):
    """Tokenize text into words"""
    return word_tokenize(text)

def remove_stopwords(tokens):
    """Remove common stopwords from token list"""
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

def prepare_sequences(tokens, seq_length):
    """Prepare sequences for LSTM model input"""
    sequences = []
    for i in range(len(tokens) - seq_length):
        seq = tokens[i:i + seq_length]
        target = tokens[i + seq_length]
        sequences.append((seq, target))
    return sequences
def remove_stopwords(tokens):
    """Remove common stopwords from token list"""
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

def prepare_sequences(tokens, seq_length):
    """Prepare sequences for LSTM model input"""
    sequences = []
    for i in range(len(tokens) - seq_length):
        seq = tokens[i:i + seq_length]
        target = tokens[i + seq_length]
        sequences.append((seq, target))
    return sequences
