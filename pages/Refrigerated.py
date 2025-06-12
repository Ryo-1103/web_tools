import streamlit as st
from PIL import Image
import io
from main import model,genai



with st.sidebar:
    st.page_link("main.py",label="ホーム",icon="🏠")
    st.page_link("pages/Refrigerated.py",label="献立の提案",icon=":material/fork_spoon:")
    st.page_link("pages/shopping_list.py",label="買い物リスト",icon=":material/shopping_cart:")

st.title('今日の献立提案')
st.write('冷蔵庫の中身かスーパーのチラシをアップロードすると、献立を提案します。')
uploaded_file = st.file_uploader("写真をアップロードしてください", type=["jpg", "jpeg", "png"])

def recognze_ingredients(input_file):

    """画像から食材を認識する関数"""
    if input_file is None:
        return "画像がアップロードされていません。" 
    
    response = model.generate_content([input_file, "日本語で写っている食材を詳細に説明してください"])

    return response.text


def suggest_recipe(ingredients):
    """食材からレシピを提案する関数"""
    prompt = (
        f"以下の食材を使って、簡単で美味しい献立２食分を提案してください。\n\n"
        f"{ingredients}\n\n"
        "レシピは日本語で、２人分の材料と手順を詳しく説明してください。"
        "また各献立ごとに【買い物リスト】を必ず作成し、"
        "各材料には必ず必要な量（例：100g、1個、少々など）を明記してください。"
        "買い物リストはマークダウン形式で「* 材料名：量」の形で出力してください。"
    )
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
    st.image(image, caption='アップロードされた画像', use_container_width=True)

    # 画像をバイナリデータに変換
    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format='PNG')
    image_byte_arr = image_byte_arr.getvalue()

    # imagesフォルダに保存（なければ作成）
    import os
    images_dir = os.path.join(os.getcwd(), "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    image_path = os.path.join(images_dir, "upload_image.png")
    with open(image_path, 'wb') as f:
        f.write(image_byte_arr) 
    input_file = genai.upload_file(path=image_path, display_name='image')

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

        # 保存ボタンをレシピの横に表示
        if st.button("この献立を保存"):
            import re
            import json

            # 買い物リストを抽出（「買い物リスト」以降の'* 'で始まる行のみ抽出）
            shopping_list = []
            match = re.search(r"買い物リスト[\s\S]+?(?:\n|$)([\s\S]+?)(?:\n\n|\Z|\*\*補足\*\*)", recipe)
            if match:
                items = match.group(1).splitlines()
                for item in items:
                    item = item.strip()
                    if item.startswith("* "):
                        shopping_list.append(item[2:].strip())
            save_data = {
                "recipe": recipe,
                "shopping_list": shopping_list
            }
            save_path = os.path.join(os.path.dirname(__file__), "shopping_data.json")
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            st.success("献立と買い物リストを保存しました！")

    else:
        st.error('レシピが見つかりません。')
