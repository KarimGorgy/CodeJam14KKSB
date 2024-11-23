import numpy
import spacy

print(f"Numpy version: {numpy.__version__}")
nlp = spacy.load("en_core_web_sm")
print("Spacy model loaded successfully!")
