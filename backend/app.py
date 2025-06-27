# backend/app.py (建議的調整)

from flask import Flask
from flask_cors import CORS
from config import Config
from api import api_bp
from extensions import db
from models import Sample

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化 extensions
    db.init_app(app)

    CORS(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    # 將 shell_context_processor 的設定也移入工廠函式中
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Sample': Sample}

    return app

# 只有在直接執行這個檔案時，才建立並運行 app
if __name__ == '__main__':
    app = create_app()
    app.run()