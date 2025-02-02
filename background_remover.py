from transformers import pipeline
from PIL import Image, ImageDraw
import requests
import streamlit as st

st.title("Background Remover (Mask)")

model_path = r'C:\Users\ompra\.vscode\No Code\Chapter_6_Code_Basics\Offline_Basics\AI_Projects\models--mattmdjaga--segformer_b2_clothes\snapshots\fc92b3abe7b123c814ca7910683151f2b7b7281e'

pipe = pipeline('image-segmentation', model=model_path)

st.write("Model loaded successfully!")

uploaded_image = st.file_uploader("Choose a photo", type=["jpg", "jpeg", "png"])
 
if st.button("Remove Background"):
    with st.spinner('Removing Background...'):
        pil_image = Image.open(uploaded_image)
        result = pipe(images=pil_image)
 
        # Background
        background = result[0]['mask']
        st.image(background, caption="Background")
       