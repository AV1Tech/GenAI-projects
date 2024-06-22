from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key for Google Generative AI is missing!")

# Function to load OpenAI model and get responses
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo", page_icon=":camera:", layout="wide")

# Page header
st.markdown("""
    <style>
        .header {
            text-align: center;
            font-size: 2.5rem;
            color: #4A90E2;
        }
        .subheader {
            text-align: center;
            font-size: 1.5rem;
            color: #34495E;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header">Gemini Application</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Analyze your food images with AI</div>', unsafe_allow_html=True)

# Input prompt
input_text = st.text_input("Enter a brief description or query:", key="input", help="Type something to get started")

# File uploader for image
uploaded_file = st.file_uploader("Upload an image (jpg, jpeg, png):", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Input prompt for AI
input_prompt = """
You are an expert nutritionist. Analyze the food items in the image and calculate the total calories. 
Provide details of each food item and their calorie content in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
---
"""

# Submit button
submit = st.button("Analyze Image")

# Spinner while processing
if submit:
    with st.spinner("Processing..."):
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_text, image_data, input_prompt)
            st.subheader("Analysis Result")
            st.success("The image has been successfully analyzed!")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown("""
    <style>
        .footer {
            text-align: center;
            font-size: 1rem;
            color: #95A5A6;
            padding: 1.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<div class="footer">&copy; 2024 Gemini AI - All Rights Reserved</div>', unsafe_allow_html=True)
