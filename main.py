import streamlit as st
import google.generativeai as genai
import calendar
import datetime
import base64

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

# --- ゴミ出しカレンダー ---
st.subheader("ゴミ出しカレンダー")


gomi_schedule = {
    0: "",    # 月曜
    1: ["images/kanen.png"],    # 火曜
    2: ["images/moenai.png", "images/shigen.png"],  # 水曜（複数画像）
    3: ["images/bin.png","images/can.png","images/petbottle.png"],      # 木曜
    4: ["images/kanen.png"],    # 金曜
    5: "",    # 土曜
    6: ""     # 日曜
}

today = datetime.date.today()
year = today.year
month = today.month

calendar_css = """
<style>
.calendar-table {
    border-collapse: collapse;
    margin-bottom: 8px;
    background: #23272f;
    color: #fff;
    width: 100%;
    max-width: 100vw;
    table-layout: fixed;
}
.calendar-table td, .calendar-table th {
    border: 1px solid #888;
    padding: 4px 0;
    width: 14vw; /* 7列で100vwに収まるように */
    height: 9vw;
    min-width: 40px;
    min-height: 40px;
    font-size: 1.3em;   /* ← 日付や文字を大きく */
    text-align: center;
    vertical-align: top;
    background: #2d323b;
    color: #fff;
    word-break: break-all;
}
.calendar-table th {
    background: #444c56;
    color: #fff;
    font-size: 1.2em;
    padding: 4px 0;
}
.gomi-label {
    display: block;
    margin-top: 2px;
    color: #b0b8c1;
    font-size: 1em;   /* ← ラベルも大きく */
}
.gomi-imgs {
    margin-top: 2px;
}
.gomi-imgs img {
    margin: 0 4px 2px 0;
    width: 48px;      /* ← 画像サイズをさらに大きく */
    height: 48px;
    vertical-align: middle;
}
.today-cell {
    background: #ff4c4c !important;
    color: #fff !important;
    border-radius: 4px;
}

/* スマホ対応: 画面幅が600px以下なら少し小さく */
@media screen and (max-width: 600px) {
    .calendar-table td, .calendar-table th {
        font-size: 1em;
        width: 13vw;
        height: 11vw;
        min-width: 28px;
        min-height: 28px;
        padding: 2px 0;
    }
    .gomi-imgs img {
        width: 32px;
        height: 32px;
    }
    .gomi-label {
        font-size: 0.85em;
    }
}
</style>
"""
st.markdown(calendar_css, unsafe_allow_html=True)

def img_to_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    ext = img_path.split('.')[-1]
    return f"data:image/{ext};base64," + base64.b64encode(data).decode()

def get_gomi_label(date, this_month):
    if date.month != this_month:
        return ""
    label = gomi_schedule.get(date.weekday(), "")
    # 画像リストの場合
    if isinstance(label, list) and label:
        imgs = "".join(
            f"<img src='{img_to_base64(img_path)}' alt='ごみ' />"
            for img_path in label
        )
        return f"<div class='gomi-imgs'>{imgs}</div>"
    # 画像1つの場合
    elif isinstance(label, str) and label.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return f"<div class='gomi-imgs'><img src='{img_to_base64(label)}' alt='ごみ' /></div>"
    elif label:
        return f"<span class='gomi-label'>{label}</span>"
    else:
        return ""

def make_calendar(year, month):
    cal = calendar.Calendar(firstweekday=6)
    calendar_rows = []
    weekdays = ["日", "月", "火", "水", "木", "金", "土"]
    # 曜日ヘッダー
    weekday_cells = []
    for i, wd in enumerate(weekdays):
        if i == 0:
            color = "red"
        elif i == 6:
            color = "deepskyblue"
        else:
            color = "#ffd700"
        weekday_cells.append(f"<b><span style='color:{color}'>{wd}</span></b>")
    calendar_rows.append(weekday_cells)
    for week in cal.monthdatescalendar(year, month):
        row = []
        for date in week:
            label = get_gomi_label(date, month)
            if date.weekday() == 6:
                color = "red"
            elif date.weekday() == 5:
                color = "deepskyblue"
            else:
                color = "#fff"
            cell_class = "today-cell" if date == today else ""
            day_str = f"<span style='color:{color}'>{date.day}</span>"
            cell = (
                f"<div class='{cell_class}' style='text-align:center;'>"
                f"<b>{day_str}</b>"
                f"{label}"
                f"</div>"
            )
            row.append(cell)
        calendar_rows.append(row)
    return calendar_rows

def render_calendar_with_images(year, month):
    cal = calendar.Calendar(firstweekday=6)
    weekdays = ["日", "月", "火", "水", "木", "金", "土"]

    # ヘッダー
    header_cols = st.columns(7)
    for i, wd in enumerate(weekdays):
        color = "red" if i == 0 else "deepskyblue" if i == 6 else "#ffd700"
        header_cols[i].markdown(f"<b><span style='color:{color}; font-size:1.3em'>{wd}</span></b>", unsafe_allow_html=True)
    # 本体
    for week in cal.monthdatescalendar(year, month):
        cols = st.columns(7)
        for i, date in enumerate(week):
            if date.month != month:
                cols[i].markdown(" ")
                continue
            # 日付
            cols[i].markdown(f"<div style='text-align:center;'><b>{date.day}</b></div>", unsafe_allow_html=True)
            # ゴミ画像
            label = gomi_schedule.get(date.weekday(), "")
            if isinstance(label, list):
                for img_path in label:
                    cols[i].image(img_path, width=48)
            elif isinstance(label, str) and label.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                cols[i].image(label, width=48)

# --- カレンダーの月送りボタン付き表示 ---

# 月・年の状態をセッションで管理
if "cal_year" not in st.session_state:
    st.session_state.cal_year = year
if "cal_month" not in st.session_state:
    st.session_state.cal_month = month

# ボタンを左右に配置
left_col, center_col, right_col = st.columns([1, 3, 1])

with left_col:
    if st.button("← 前月", key="prev_month"):
        if st.session_state.cal_month == 1:
            st.session_state.cal_month = 12
            st.session_state.cal_year -= 1
        else:
            st.session_state.cal_month -= 1

with right_col:
    if st.button("翌月 →", key="next_month"):
        if st.session_state.cal_month == 12:
            st.session_state.cal_month = 1
            st.session_state.cal_year += 1
        else:
            st.session_state.cal_month += 1

with center_col:
    st.markdown(
        f"<div style='text-align:center;font-size:2em;font-weight:bold;'>{st.session_state.cal_year}年{st.session_state.cal_month}月</div>",
        unsafe_allow_html=True
    )

# カレンダー本体をHTMLテーブルで表示
def render_calendar_with_html(year, month):
    calendar_rows = make_calendar(year, month)
    st.markdown(
        "<table class='calendar-table'>" +
        "".join(
            "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
            for row in calendar_rows
        ) +
        "</table>",
        unsafe_allow_html=True
    )

# カレンダー本体を表示
render_calendar_with_html(st.session_state.cal_year, st.session_state.cal_month)