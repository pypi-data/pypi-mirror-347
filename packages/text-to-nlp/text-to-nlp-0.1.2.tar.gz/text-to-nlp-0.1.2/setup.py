from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text-to-nlp",
    version="0.1.2",
    packages=find_packages(),
    install_requires=['nltk', 'scikit-learn'],
    author="Mehdi Omidi",
    author_email="mohammadmehdiomidi95@gmail.com",
    description="A simple text preprocessing package for NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moraix/text_preprocessor"
)