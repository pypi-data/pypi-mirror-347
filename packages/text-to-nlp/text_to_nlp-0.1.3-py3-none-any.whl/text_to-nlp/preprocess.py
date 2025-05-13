import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import string

nltk.download('punkt')
nltk.download('stopwords')

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text):
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if token.isalnum() and token not in self.stop_words]
        return ' '.join(tokens)

    def to_tfidf(self, texts):
        vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1,2))
        tfidf_matrix = vectorizer.fit_transform(texts)
        return tfidf_matrix, vectorizer