import sys
from pathlib import Path
from PIL import Image
import streamlit as st
from transformers import pipeline


st.title("AI Photo Semantic Finder")


@st.cache_resource
def load_model():
    
    return pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")


model = load_model()


uploaded_image = st.file_uploader("Choose a photo", type=["jpg", "jpeg", "png"])

if st.button("Generate Semantics"):
    if uploaded_image is not None:
        with st.spinner("Generating Semantics..."):
            try:
    
                col1, col2 = st.columns(2)
                with col1:
                    st.image(uploaded_image, width=300)

    
                pil_image = Image.open(uploaded_image)
                semantics = model(images=pil_image)[0]['generated_text']

    
                with col2:
                    st.subheader("Generated Semantics")
                    st.write(semantics)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an image to proceed.")