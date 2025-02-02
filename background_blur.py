from transformers import pipeline
from PIL import Image, ImageDraw
import requests
import streamlit as st
from PIL import Image, ImageFilter, ImageOps

st.title("AI Background Blurring Tool")

model_path = r'C:\Users\ompra\.vscode\No Code\Chapter_6_Code_Basics\Offline_Basics\AI_Projects\models--mattmdjaga--segformer_b2_clothes\snapshots\fc92b3abe7b123c814ca7910683151f2b7b7281e'

pipe = pipeline('image-segmentation', model=model_path)

st.write("Model loaded successfully!")

uploaded_image = st.file_uploader("Choose a photo", type=["jpg", "jpeg", "png"])

if uploaded_image:
    with st.spinner('Adding Blur...'):
        blur_level = st.slider("Adjust Blur Level", min_value=0, max_value=30, value=15, step=1)
 
        original = Image.open(uploaded_image)
        result = pipe(images=original)
 
        mask = result[0]['mask']
 
 
        mask_original = Image.composite(original, Image.new('RGB', original.size, 0), mask)
 
        mask_original_blur = mask_original.filter(ImageFilter.GaussianBlur(radius=blur_level))
     
        mask_inverted = ImageOps.invert(mask)
         
        mask_inverted_original = Image.composite(original,
                                                 Image.new('RGB', original.size, 0), mask_inverted)
         
        final_image = Image.composite(mask_inverted_original, mask_original_blur, mask_inverted)
        st.image(final_image, caption="final_image")