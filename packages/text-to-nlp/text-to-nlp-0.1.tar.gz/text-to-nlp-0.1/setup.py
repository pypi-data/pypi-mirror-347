from setuptools import setup, find_packages

setup(
    name="text-to-nlp",
    version="0.1",
    packages=find_packages(),
    install_requires=['nltk', 'scikit-learn'],
    author="Mehdi Omidi",
    author_email="mohammadmehdiomidi95@gmail.com",
    description="A simple text preprocessing package for NLP",
    url="https://github.com/moraix/text_preprocessor"
)