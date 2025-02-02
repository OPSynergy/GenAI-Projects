import streamlit as st
from transformers import pipeline
from PIL import Image
import google.generativeai as genai
from api_key import api
import os
import uuid
import sys 
from pathlib import Path

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

def get_image_semantics(image):
    semantics = model(images=image)[0]['generated_text']
    return semantics
 

def rename_and_save_image(image, save_path, semantics):
    if image.mode != 'RGB':
        image = image.convert('RGB') 
    new_file_name = f"{uuid.uuid4()}_{semantics}.jpg"
    new_save_path = os.path.join(Path(save_path), new_file_name)
    image.save(new_save_path)
    return new_save_path

def save_and_process_files(uploaded_files, upload_dir):
    progress_bar = st.progress(0)  
    count = st.empty()  
    for i,uploaded_file in enumerate(uploaded_files):
        image = Image.open(uploaded_file)  
        semantics = get_image_semantics(image)  
 
        
        rename_and_save_image(image, upload_dir, semantics)
        progress_bar.progress(int((i+1)/len(uploaded_files)*100))  
        count.text(f"{i+1}/{len(uploaded_files)} images processed")

def get_image_files(upload_dir):
    return [os.path.join(upload_dir, filename)  
            for filename in os.listdir(upload_dir)  
            if filename.endswith(('.png', '.jpg'))] 

def filter_images(search_query, upload_dir):
    image_files = get_image_files(upload_dir)  
    if search_query:
        keywords = search_query.lower().split()  
        filtered_files = [file for file in image_files if all(keyword in Path(file).stem.lower() for keyword in keywords)]
        return filtered_files
    else:
        return image_files
    


st.title("AI Based Google Photos Replica")
model_path = r'C:\Users\ompra\.vscode\No Code\Chapter_6_Code_Basics\Offline_Basics\Models\models--Salesforce--blip-image-captioning-base\snapshots\89b09ea1789f7addf2f6d6f0dfc4ce10ab58ef84'
@st.cache_resource
def load_model():
    return pipeline("image-to-text", model=model_path)

model = load_model()

upload_dir = 'uploaded_images'
os.makedirs(upload_dir, exist_ok=True)
 

if 'file_uploader_key' not in st.session_state:
    st.session_state['file_uploader_key'] = uuid.uuid4().hex
 
 
uploaded_images = st.file_uploader("Choose a photo",accept_multiple_files=True,
                                   type=["jpg", "jpeg", "png"], key=st.session_state['file_uploader_key'])
 
if uploaded_images:
    save_and_process_files(uploaded_images, upload_dir)
    st.session_state['file_uploader_key'] = uuid.uuid4().hex

def display_images_in_grid(image_files):
    if image_files:
        num_cols = 3  # Number of columns in the grid.
        cols = st.columns(num_cols)  # Create columns.
        for index, file_path in enumerate(image_files):
            image = Image.open(file_path)  # Open the image file.
            cols[index % num_cols].image(image, use_container_width=True)

search_query = st.text_input("Search Images")
# Filter and display images based on the search query.
filtered_files = filter_images(search_query, upload_dir)
display_images_in_grid(filtered_files)