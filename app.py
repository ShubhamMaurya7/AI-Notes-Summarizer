import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pdfplumber
import docx

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="AI Notes Summarizer", layout="wide")
st.title("📚 AI Notes Summarizer")

input_type = st.radio("Choose Input Type:", ["Paste Text", "Upload PDF", "Upload DOCX"])
user_input = ""

if input_type == "Paste Text":
    user_input = st.text_area("Paste your notes here:")
elif input_type == "Upload PDF":
    uploaded_file = st.file_uploader("Upload PDF File", type="pdf")
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            user_input = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
elif input_type == "Upload DOCX":
    uploaded_file = st.file_uploader("Upload DOCX File", type="docx")
    if uploaded_file:
        doc = docx.Document(uploaded_file)
        user_input = "\n".join([para.text for para in doc.paragraphs])

if st.button("🔍 Summarize"):
    if user_input.strip() != "":
        prompt = f"Summarize the following notes:\n\n{user_input}"
        response = model.generate_content(prompt)
        st.subheader("📝 Summary")
        st.write(response.text)
    else:
        st.warning("Please provide or upload some notes.")
