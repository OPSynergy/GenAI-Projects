from PIL import Image
import streamlit as st
from transformers import pipeline
 
st.title("AI Adult Content Detector")
model_path = r'C:\Users\ompra\.vscode\No Code\Chapter_6_Code_Basics\Offline_Basics\AI_Projects\models--Falconsai--nsfw_image_detection\snapshots\63e0a066bb08d2ae47324b540fba3adfd4536569'
 
model = pipeline('image-classification',model= model_path)
 
image_path = r"C:\Users\ompra\.vscode\No Code\Chapter_6_Code_Basics\Offline_Basics\AI_Projects\OP.jpg"
 
with st.spinner('Checking Content...'):
    pil_image = Image.open(image_path)
    result = model(images=pil_image)
    nsfw_score = next((item['score'] for item in result if item['label'] == 'nsfw'), None)
    st.write(nsfw_score)
 
    st.subheader("Adult Content Probability : " + str(round(nsfw_score * 100, 2)) + "%")
    st.slider("",0,100, int(nsfw_score*100),1)
 
    if nsfw_score > 0.1:
        st.subheader("Your Content is not safe")
        st.text("Cannot Display the Image")
    else:
        st.subheader("Your Content is safe")
        st.image(pil_image)