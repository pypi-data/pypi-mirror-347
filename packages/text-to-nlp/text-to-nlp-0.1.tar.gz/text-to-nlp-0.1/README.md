# Text Preprocessor
A simple Python package for NLP text preprocessing.

## Installation
```bash
pip install text-to-nlp
```

## Usage
```python
from text_preprocessor import TextPreprocessor
processor = TextPreprocessor()
text = "I am running and jumping happily!"
print(processor.preprocess(text))  # Output: running jumping happily
texts = ["I am running happily", "Jumping is fun"]
tfidf_matrix, vectorizer = processor.to_tfidf(texts)
print(tfidf_matrix.toarray().shape)
```