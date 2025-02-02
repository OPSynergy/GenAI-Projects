from api_key import api
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

st.title("AI Recipe Generator")

recipe = st.text_input("Enter your prompt: ", value='Chicken Biryani')

genai.configure(api_key=api)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

if st.button("Create Recipe"):
    with st.spinner("Generating recipe and image..."):
        try:
           
            payload = {"inputs": recipe}
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="Generated Recipe Image")
            else:
                st.error(f"Image generation error: {response.text}")

            text_area_placeholder = st.empty()
            prompt = f"Create a detailed recipe for {recipe}."
            recipe_response = chat_session.send_message(prompt)

           
            text_area_placeholder.text_area("Generated Recipe:", value=recipe_response.text, height=300)

        except Exception as e:
            st.error(f"An error occurred: {e}")