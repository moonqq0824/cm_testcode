# backend/api/__init__.py (更新後)

from flask import Blueprint
from flask_restx import Api
from .charts import ns as charts_ns 
from .wastewater_reports import ns as wastewater_reports_ns
from .samples import ns as samples_ns
from .statistics import ns as statistics_ns 

api_bp = Blueprint('api', __name__)

api = Api(api_bp,
          title='CM-Test-Code API',
          version='1.0',
          description='一個使用 Flask-RESTx 建構的示範 API',
          doc='/docs'
         )

# 將匯入的 Namespace 註冊到我們的 Api 物件
api.add_namespace(samples_ns, path='/v1/samples')
api.add_namespace(statistics_ns, path='/v1/statistics') 
api.add_namespace(charts_ns, path='/v1/charts')
api.add_namespace(wastewater_reports_ns, path='/v1/wastewater-reports')