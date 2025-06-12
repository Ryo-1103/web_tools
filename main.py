import streamlit as st
import google.generativeai as genai

from config import config

genai.configure(api_key=config.API_KEY)  # Replace with your actual API key
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.set_page_config(
    page_title="メインページ",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)
with st.sidebar:
    st.page_link("main.py",label="ホーム",icon="🏠")
    st.page_link("pages/Refrigerated.py",label="献立の提案",icon=":material/fork_spoon:")
    st.page_link("pages/shopping_list.py",label="買い物リスト",icon=":material/shopping_cart:")

st.title("メインページ")