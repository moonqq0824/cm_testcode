# backend/app.py

from flask import Flask
from flask_cors import CORS
from config import Config
from api import api_bp # 從 api 套件匯入我們的 Blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 啟用 CORS，允許所有來源的請求（在開發階段很方便）
    CORS(app)

    # 註冊 API 藍圖，並設定 URL 前綴為 /api
    # 最終 API 的完整路徑會是 /api/v1/samples
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

# 為了讓 .flaskenv 能正確找到 app
app = create_app()

if __name__ == '__main__':
    app.run()