# backend/api/__init__.py

from flask import Blueprint
from flask_restx import Api
from .samples import SampleList

# 建立一個 Blueprint
api_bp = Blueprint('api', __name__)

# 將 Blueprint 交給 Api 物件進行管理
# doc='/docs' 可以讓 Swagger UI 文件產生在 /api/docs 路徑下
api = Api(api_bp,
          title='CM-Test-Code API',
          version='1.0',
          description='A demo API for CM-Test-Code project',
          doc='/docs'
         )

# 為 API 加上 Namespace，並將我們寫好的 Resource 加入
# 這樣我們的 API 路徑就會是 /v1/samples
ns = api.namespace('v1', description='Version 1 APIs')
ns.add_resource(SampleList, '/samples')