# ゴミ出し管理アプリ

## 概要
このアプリケーションは、以下の機能を提供します：
- ゴミ出しカレンダー（曜日ごとのゴミの種類を表示）
- 献立提案機能（冷蔵庫の中身から献立を提案）
- 買い物リスト管理

## 必要要件
- Python 3.8以上
- Streamlit
- Google Gemini API Key

## インストール方法
```bash
git clone https://github.com/yourusername/web_tools.git
cd web_tools
pip install -r requirements.txt
```

## 環境設定
1. `.streamlit/secrets.toml`ファイルを作成
2. 以下の内容を追加：
```toml
GEMINI_API_KEY = "あなたのGemini APIキー"
```

## 使用方法
```bash
streamlit run main.py
```

## ディレクトリ構造
```
web_tools/
├── README.md
├── requirements.txt
├── main.py                # メインアプリケーション
├── pages/                 # 追加ページ
│   ├── Refrigerated.py    # 献立提案
│   └── shopping_list.py   # 買い物リスト
├── images/                # ゴミアイコン画像
└── .streamlit/           # Streamlit設定
    └── secrets.toml      # API Key（非公開）
```

## ライセンス
MIT License