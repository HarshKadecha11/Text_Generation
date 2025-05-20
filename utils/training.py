import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

def create_word_indices(tokens):
    """Create word-to-index and index-to-word mappings"""
    # Get unique words
    unique_words = sorted(list(set(tokens)))
    
    # Create mappings
    word_to_idx = {word: idx for idx, word in enumerate(unique_words)}
    idx_to_word = {idx: word for idx, word in enumerate(unique_words)}
    
    return word_to_idx, idx_to_word, len(unique_words)

def prepare_training_data(sequences, word_to_idx, vocab_size):
    """Convert sequences to training data format"""
    X = []
    y = []
    
    for seq, target in sequences:
        # Convert input sequence to indices
        X.append([word_to_idx.get(word, 0) for word in seq])
        
        # Convert target to one-hot encoded vector
        target_idx = word_to_idx.get(target, 0)
        y.append(to_categorical(target_idx, num_classes=vocab_size))
    
    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    
    # Split into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_val, y_train, y_val

def load_sample_data():
    """Load a small sample of text data for demonstration purposes"""
    sample_text = """
    Artificial intelligence is the simulation of human intelligence processes by machines, 
    especially computer systems. These processes include learning, reasoning, and self-correction.
    Applications of AI include advanced web search engines, recommendation systems, 
    natural language processing, and autonomous vehicles.
    
    Machine learning is a subset of AI that provides systems the ability to automatically learn 
    and improve from experience without being explicitly programmed. Deep learning is a further 
    subset that uses neural networks with many layers.
    
    Natural language processing is concerned with the interactions between computers and human language, 
    particularly how to program computers to process and analyze large amounts of natural language data.
    """
    return sample_text
