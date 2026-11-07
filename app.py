import os
import streamlit as st
from google import genai

# Read API key from Streamlit Cloud Secrets
API_KEY = st.secrets.get(
    "GOOGLE_API_KEY",
    os.getenv("GOOGLE_API_KEY", "")
)

if not API_KEY:
    st.error("Gemini API key is missing. Check Streamlit Secrets.")
    st.stop()

# Configure Gemini
client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"


def generate_gemini_response(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Gemini API error: {str(e)}"