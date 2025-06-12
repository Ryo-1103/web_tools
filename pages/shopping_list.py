import streamlit as st
import os
import json
import re

st.set_page_config(
    page_title="買い物リスト",
    page_icon=":material/shopping_cart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.page_link("main.py",label="ホーム",icon="🏠")
    st.page_link("pages/Refrigerated.py",label="献立の提案",icon=":material/fork_spoon:")
    st.page_link("pages/shopping_list.py",label="買い物リスト",icon=":material/shopping_cart:")

st.title("買い物リスト")

save_path = os.path.join(os.path.dirname(__file__), "shopping_data.json")

if os.path.exists(save_path):
    with open(save_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    st.write(data.get("recipe", ""))

    shopping_list = data.get("shopping_list", [])

    # 材料名ごとに量をまとめる
    ingredient_dict = {}
    for item in shopping_list:
        # 「材料名：量」形式を分割
        parts = re.split(r"[:：]", item, maxsplit=1)
        if len(parts) == 2:
            name = parts[0].strip()
            amount = parts[1].strip()
        else:
            name = item.strip()
            amount = ""
        if name in ingredient_dict:
            ingredient_dict[name].append(amount)
        else:
            ingredient_dict[name] = [amount]

    # チェック状態の管理
    if "checked" not in st.session_state or len(st.session_state.checked) != len(ingredient_dict):
        st.session_state.checked = [False] * len(ingredient_dict)

    for i, (name, amounts) in enumerate(ingredient_dict.items()):
        amount_str = ", ".join([a for a in amounts if a])
        label = f"{name}：{amount_str}" if amount_str else name
        # カラム幅を狭くする（例: 0.03, 0.97）
        col1, col2 = st.columns([0.01, 0.97])
        with col1:
            checked = st.checkbox("", value=st.session_state.checked[i], key=f"item_{i}")
            st.session_state.checked[i] = checked
        with col2:
            st.markdown(
                f"<div style='line-height:2.2'>{'<s>' + label + '</s>' if checked else label}</div>",
                unsafe_allow_html=True
            )

else:
    st.info("保存された買い物リストがありません。")