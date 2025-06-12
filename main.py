import streamlit as st
from PIL import Image
import io
import google.generativeai as genai

genai.configure(api_key="API_KEY")  # Replace with your actual API key
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.set_page_config(page_title='今日の献立提案',  layout='wide')
st.title('今日の献立提案')
st.write('冷蔵庫の中身の写真をアップロードすると、今日の献立を提案します。')

uploaded_file = st.file_uploader("冷蔵庫の中身の写真をアップロードしてください", type=["jpg", "jpeg", "png"])

def recognze_ingredients(input_file):

    """画像から食材を認識する関数"""
    if input_file is None:
        return "画像がアップロードされていません。" 
    
    response = model.generate_content([input_file, "日本語で写っている食材を詳細に説明してください"])

    return response.text


def suggest_recipe(ingredients):
    """食材からレシピを提案する関数"""
    prompt = f"以下の食材を使って、簡単で美味しいレシピを提案してください。\n\n{ingredients}\n\nレシピは日本語で、材料と手順を詳しく説明してください。"+ ingredients

    response = model.generate_content(prompt)

    if response:
        return response.text
    else:
        st.error("レシピの提案に失敗しました。もう一度試してください。")
        return None
    
if uploaded_file is not None:
    # 画像を読み込む
    image = Image.open(uploaded_file)
    
    # 画像を表示
    st.image(image, caption='アップロードされた画像', use_column_width=True)

    # 画像をバイナリデータに変換
    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format='PNG')
    image_byte_arr = image_byte_arr.getvalue()

    with open('uploaded_fridge_image.png', 'wb') as f:
        f.write(image_byte_arr) 
    input_file = genai.upload_file(path=r'C:\Users\hryo-un\Desktop\cook\uploaded_fridge_image.png', display_name = 'image')

    with st.spinner('食材を認識中...'):
        ingredients = recognze_ingredients(input_file)

    if ingredients:
        st.write("認識された食材:")
        st.write(ingredients)

    with st.spinner('レシピを提案中...'):
        recipe = suggest_recipe(ingredients)

    if recipe:
        st.write("こちらがいくつかのレシピ提案です")
        st.write(recipe)

    else:
        st.error('レシピが見つかりません。')
