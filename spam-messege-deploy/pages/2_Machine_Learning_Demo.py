import streamlit as st
import joblib
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize PorterStemmer
ps = PorterStemmer()

# Function to preprocess text
@st.cache_data
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    
    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
    
    return " ".join(y)

# Load the TF-IDF vectorizer and model using joblib
@st.cache_data
def load_model():
    with open('model/feature_extraction.joblib', 'rb') as file:
        tfidf = joblib.load(file)

    with open('model/random_forest_model.joblib', 'rb') as file:
        model = joblib.load(file)

    return tfidf, model

# Streamlit app title
st.title('Email/SMS Spam Checker')

# Input text field for user
input_sms = st.text_input('Enter the Message')

# Predict button
if st.button('CHECK MESSAGE'):
    if input_sms.strip():  # Ensure input is not empty
        transform_sms = transform_text(input_sms)
        tfidf, model = load_model()  # Load model and TF-IDF vectorizer
        vector_input = tfidf.transform([transform_sms])
        result = model.predict(vector_input)[0]

        if result == 1:
            st.header("NOT SPAM!")
        else:
            st.header('SPAM!')
    else:
        st.warning('Please enter a message to predict.')
