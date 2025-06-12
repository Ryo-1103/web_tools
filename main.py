import streamlit as st
import google.generativeai as genai

from config import config

genai.configure(api_key=config.API_KEY)  # Replace with your actual API key
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


with st.sidebar:
    st.page_link("main.py",label="ホーム",icon="🏠")
    st.page_link("pages/Refrigerated.py",label="冷蔵庫の中身",icon=":material/kitchen:")
    st.page_link("pages/super_flyer.py",label="スーパーのチラシ",icon=":material/storefront:")

st.title("メインページ")