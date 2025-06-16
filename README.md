# ホーム管理アプリ

## 機能
- ゴミ出しカレンダー：曜日ごとのゴミの種類を視覚的に表示
- 献立提案：冷蔵庫の中身から最適な献立を提案
- 買い物リスト管理：提案された献立の材料をチェックリストで管理

## 必要要件
- Python 3.8以上
- Streamlit
- Google Gemini API Key

## インストール方法
```bash
git clone https://github.com/hryo-un/web_tools.git
cd web_tools
pip install -r requirements.txt
```

## 環境設定
1. `.streamlit/secrets.toml`ファイルを作成
2. 以下の内容を追加：
```toml
GEMINI_API_KEY = "your-api-key"
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