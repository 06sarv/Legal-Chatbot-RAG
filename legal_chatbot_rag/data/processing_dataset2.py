import pandas as pd 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

ipc_df = pd.read_csv("ipc_sections.csv")  


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    words = word_tokenize(text.lower())  
    processed_words = [
        lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words
    ]
    return " ".join(processed_words)


ipc_df['processed_description'] = ipc_df['Description'].apply(preprocess_text)
print(ipc_df[['Description', 'processed_description']].head())

import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download necessary NLTK data if not already done
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Preprocess function
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords and apply lemmatization
    cleaned_tokens = [
        lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and word.isalpha()
    ]

    # Join tokens back into a string
    return ' '.join(cleaned_tokens)

# Apply preprocessing to 'Description' column
ipc_df['processed_description'] = ipc_df['Description'].apply(preprocess_text)

# Inspect the processed data
print(ipc_df[['Description', 'processed_description']].head())

