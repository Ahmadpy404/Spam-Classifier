import streamlit as st
import pickle

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Title
st.title("📩 Spam Message Classifier")

# Description
st.write("Enter a message to check whether it is Spam or Not Spam.")

# Input box
user_input = st.text_area("Enter your message:")

# Button
if st.button("Check"):
    if user_input.strip() == "":
        st.warning("Please enter a message")
    else:
        # Transform input
        data = vectorizer.transform([user_input])

        # Predict
        prediction = model.predict(data)

        # Output
        if prediction[0] == 1:
            st.error("🚨 This is a Spam Message")
        else:
            st.success("✅ This is Not Spam")