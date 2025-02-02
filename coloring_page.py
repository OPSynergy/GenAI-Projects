from api_key import api
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import streamlit as st
import requests

st.title("AI Coloring Page")

API_URL = "Your api"
headers = {"Authorization": "Bearer your_authorixation header"}

user_input = st.text_input("Enter your prompt", value="lion")

num_images = st.slider("Select number of images to generate:", 1, 10, 2)

if st.button("Generate Image"):
    with st.spinner("Generating image..."):
        progress_bar = st.progress(0)

        for i in range(num_images):
            if i % 2 == 0:
                cols = st.columns(2)

        try:
            payload = {"inputs": user_input}
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=user_input)
            else:
                st.error(f"Image generation error: {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")