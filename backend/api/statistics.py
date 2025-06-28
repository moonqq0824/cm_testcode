# backend/api/statistics.py

from flask_restx import Namespace, Resource
from sqlalchemy import func
from models import Sample
from extensions import db

ns = Namespace('statistics', description='統計數據相關操作')

@ns.route('/main-metrics')
class MainMetrics(Resource):
    def get(self):
        """獲取關鍵製程指標"""
        
        # 使用 SQLAlchemy 的 func 來執行 SQL 彙總函式
        total_records = db.session.query(func.count(Sample.id)).scalar()
        avg_metric_a = db.session.query(func.avg(Sample.metric_a)).scalar()
        avg_metric_b = db.session.query(func.avg(Sample.metric_b)).scalar()
        latest_record_time = db.session.query(func.max(Sample.timestamp)).scalar()
        
        # 處理可能的空資料庫情況
        if total_records == 0:
            return {
                'total_records': 0,
                'avg_metric_a': 0,
                'avg_metric_b': 0,
                'latest_record_time': None
            }
            
        return {
            'total_records': total_records,
            'avg_metric_a': round(avg_metric_a, 2) if avg_metric_a else 0,
            'avg_metric_b': round(avg_metric_b, 2) if avg_metric_b else 0,
            'latest_record_time': latest_record_time.isoformat() if latest_record_time else None
        }