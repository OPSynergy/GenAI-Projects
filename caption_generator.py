import streamlit as st
from transformers import pipeline
from PIL import Image
import google.generativeai as genai
from api_key import api

st.title("AI Image Caption Generator")
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

chat_session = model.start_chat(
    history=[]
)

@st.cache_resource
def load_model():
    return pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

model = load_model()

uploaded_image = st.file_uploader("Upload an image (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Image")

    if st.button("Generate Caption"):
        with st.spinner("Generating caption..."):
            try:
                pil_image = Image.open(uploaded_image)
                semantics_result = model(images=pil_image)
                semantics = semantics_result[0]['generated_text']

                st.subheader("Generated Image Caption:")
                st.write(semantics)

                prompt = (f"Based on the image description, generate 3 captions for Instagram and add the hashtags "
                          f"Here is the description: {semantics} .List only the captions in json format like 1: Caption1 2:Caption2 ... ")
                
                response = chat_session.send_message(prompt)
                print(response)
                st.markdown(response)                

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an image to proceed.")