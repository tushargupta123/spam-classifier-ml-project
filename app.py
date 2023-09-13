import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

def transform_text(text):
    text = text.lower() # lower case

    text = nltk.word_tokenize(text) # tokenize text

    y=[]

    for i in text:
        if i.isalnum():
            y.append(i) # removing special characters

    text=y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i) # removing stop words and punctuation

    text=y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))    # stemming

    return " ".join(y)

st.title('SMS Spam Classifier')
input_sms=st.text_area("Enter the message")

if st.button('Predict'):
    transformed_text = transform_text(input_sms)
    vector_input = tfidf.transform([transformed_text])
    result=model.predict(vector_input)[0]
    if result==1:
        st.header("Spam")
    else:
        st.header("Not Spam")



