# Text to NLP
A simple and efficient Python package for text preprocessing in Natural Language Processing (NLP).

## Features
- Tokenizes text into words.
- Removes stop words (e.g., "the", "is").
- Removes punctuation marks (e.g., "!", ".", ",").
- Converts text to TF-IDF vectors for machine learning.

## Requirements
- Python 3.6+
- nltk>=3.8.1
- scikit-learn>=1.3.0

## Installation
```bash
pip install text-to-nlp
```

## Usage
```python
from text_preprocessor import TextPreprocessor

# Initialize the preprocessor
processor = TextPreprocessor()

# Preprocess a single text
text = "I am running, jumping happily!!!"
processed_text = processor.preprocess(text)
print("Processed text:", processed_text)  # Output: running jumping happily

# Convert multiple texts to TF-IDF
texts = ["I am running happily!", "Jumping is fun?", "Sad days are bad."]
tfidf_matrix, vectorizer = processor.to_tfidf(texts)
print("TF-IDF matrix shape:", tfidf_matrix.toarray().shape)  # Output: (3, 1000)
```