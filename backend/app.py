# backend/app.py (最終版)

from flask import Flask
from flask_cors import CORS
from config import Config
from api import api_bp
from extensions import db, bcrypt, jwt
from models import Sample, WastewaterReport, WastewaterReportItem, User
from datetime import datetime

def create_app():
    app = Flask(__name__)
    # 這是解決 CORS Redirect 問題的關鍵
    app.url_map.strict_slashes = False 
    app.config.from_object(Config)

    # 初始化 extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 註冊 API 藍圖
    app.register_blueprint(api_bp)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db, 
            'Sample': Sample,
            'WastewaterReport': WastewaterReport,
            'WastewaterReportItem': WastewaterReportItem,
            'User': User
        }

    return app

app = create_app()

@app.cli.command('seed-db')
def seed_db_command():
    """Seeds the database with initial test data."""
    print("Seeding database...")
    try:
        # ... (seed-db 的內容不變) ...
        print("Database seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")

if __name__ == '__main__':
    app.run()