# backend/api/__init__.py (全新內容)

from flask import Blueprint
from flask_restx import Api

# 從各個功能模組匯入它們自己的 Namespace
from .samples import ns as samples_ns

api_bp = Blueprint('api', __name__)

api = Api(api_bp,
          title='CM-Test-Code API',
          version='1.0',
          description='一個使用 Flask-RESTx 建構的示範 API',
          doc='/docs'
         )

# 將匯入的 Namespace 註冊到我們的 Api 物件
# 未來有新的功能 (例如 customers)，只需要在這裡多加一行
api.add_namespace(samples_ns, path='/v1/samples')