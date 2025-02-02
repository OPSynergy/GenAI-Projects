import google.generativeai as genai
import streamlit as st
from api_key import api  

st.title("AI Meal Planner")


genai.configure(api_key=api)


col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox('Gender', ('Male', 'Female', 'Others'))
    weight = st.number_input('Weight (kg):', min_value=30, max_value=200, value=80)

with col2:
    age = st.number_input('Age:', min_value=1, max_value=200, value=30)
    height = st.number_input('Height (cm):', min_value=1, max_value=250, value=170)


aim = st.selectbox('Aim', ('Lose', 'Gain', 'Maintain'))
preference = st.selectbox('Choose your preference',('Veg','Non-Veg'))


user_data = f"""-I am a {gender}.
                - My weight is {weight} kg.
                - I am {age} years old.
                - My height is {height} cm.
                - My aim is to {aim} weight.
                - My preference is {preference} type of food
            """

output_format = """
{
    "range": "Range of ideal weight",
    "target": "Target weight",
    "difference": "Weight to lose or gain",
    "bmi": "My BMI",
    "meal_plan": "Meal plan for 7 days",
    "total_days": "Total days to reach target weight",
    "weight_per_week": "Weight to lose or gain per week"
}
"""

prompt = user_data + (
    " Given the information, follow the output format as follows."
    " Give only JSON format, nothing else." + output_format
)


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

if st.button("Generate Meal Plan"):
    with st.spinner('Creating meal plan...'):
        try:
            response = chat_session.send_message(prompt)
            st.text_area("Generated Meal Plan (JSON):", value=response.text, height=300)
        except Exception as e:
            st.error(f"An error occurred: {e}")