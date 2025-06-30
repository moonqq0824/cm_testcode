# backend/api/__init__.py (最終版)

from flask import Blueprint
from flask_restx import Api
from flask_cors import CORS

# 從各個功能模組匯入它們自己的 Namespace
from .samples import ns as samples_ns
from .statistics import ns as statistics_ns
from .charts import ns as charts_ns
from .wastewater_reports import ns as wastewater_reports_ns
from .auth import ns as auth_ns

# 建立一個總的 API 藍圖
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# 將 CORS 直接作用在 api_bp 這個藍圖上，並提供最詳細的設定
CORS(api_bp, resources={
    r"/*": { # r"/*" 代表此藍圖下的所有路徑
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

authorizations = {
    'jsonWebToken': {
        'type': 'apiKey', 'in': 'header', 'name': 'Authorization',
        'description': "請在輸入框中輸入 'Bearer ' (並加上一個空格)，然後再貼上你的 JWT token。"
    }
}

api = Api(api_bp,
          title='CM-Test-Code API',
          version='1.0',
          description='一個使用 Flask-RESTx 建構的示範 API',
          doc='/docs',
          authorizations=authorizations,
         )

# 註冊所有 Namespaces，路徑由 Namespace 名稱和 @ns.route() 決定
api.add_namespace(auth_ns)
api.add_namespace(samples_ns)
api.add_namespace(statistics_ns)
api.add_namespace(charts_ns)
api.add_namespace(wastewater_reports_ns)