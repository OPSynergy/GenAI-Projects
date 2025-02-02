from pypdf import PdfReader
import os
import streamlit as st
import google.generativeai as genai
from api_key import api

st.title("AI PDF Sorter")

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

output_folder = "Organized"


files = st.file_uploader("Choose a file", type="pdf", accept_multiple_files=True)

if st.button("Organize PDFs"):
    with st.spinner("Working on PDFs"):
        for i, file in enumerate(files):
            
            reader = PdfReader(file)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            raw_text = page.extract_text()

            
            output_format = 'title - keyword - keyword - ....'
            prompt = (
                "Below is the text of a research paper. I want you to generate a name for the papers that has "
                "the full name of the paper as well as 3 keywords that will allow me to find it later. "
                "If there are any special characters in the text like : / \\ or other, remove them from the title. "
                "Give raw text as the output in the following format: "
                f"{output_format}\n\"\"\"{raw_text}\"\"\""
            )

            response = chat_session.send_message(prompt)
            generated_text = response.text.strip()
            cleaned_text = ''.join(c for c in generated_text if c.isalnum() or c in [' ', '-', '_'])

            st.subheader(f"PDF {i + 1}")
            st.write("Title: " + cleaned_text)

            os.makedirs(output_folder, exist_ok=True)
            new_file_path = f"{output_folder}/{cleaned_text}.pdf"

            
            with open(new_file_path, "wb") as f:
                f.write(file.getbuffer())