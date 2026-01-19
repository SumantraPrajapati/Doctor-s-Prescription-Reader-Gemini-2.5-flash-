import streamlit as st
from PIL import Image
import os 
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()


genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))


def get_gemini_response(input , image , prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([input , image[0] , prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type":uploaded_file.type , "data":bytes_data}]
    else:
        return FileNotFoundError("No image uploaded")

st.set_page_config(page_title = "Gemini Medical Prescription Reader")
st.header("Medical Prescription Analyser")
input = st.text_input("Ask questions about the prescription" , key = "input")
uploaded_file = st.file_uploader("Upload a Medical Prescription image", type = ["png" , "jpg" , "jpeg"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image , caption = "Uploaded Image" , use_column_width = True)

submit = st.button("Analyze Prescription")


input_prompt = """
You are a medical prescription analysis expert.
You will receive an image contraining doctor's handwritten
or printed prescription.

Your task is to:
1. Read and interpret the medicines
2. Identify the dosage and frequency
3. Extract Patient name , doctor name , date if available
4. Extract additions; notest like dietary instructinos or warnings.
5. If handwritten text is unclear , write "some text is not readable"
Always provide the final output in a clean and structured format.
"""
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt , image_data , input)
    st.subheader("The response is ")
    st.write(response)



