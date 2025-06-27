# backend/config.py (更新後)
import os

# 取得專案的根目錄路徑
basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    """基礎設定類別"""
    DEBUG = True
    # 設定資料庫連線 URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # 關閉 Flask-SQLAlchemy 的事件通知系統，以節省資源
    SQLALCHEMY_TRACK_MODIFICATIONS = False