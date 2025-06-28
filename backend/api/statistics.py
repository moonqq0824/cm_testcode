# backend/api/statistics.py

from flask_restx import Namespace, Resource
from sqlalchemy import func
from models import Sample
from extensions import db

ns = Namespace('statistics', description='統計數據相關操作')

@ns.route('/main-metrics')
class MainMetrics(Resource):
    def get(self):
        """獲取關鍵製程指標，包含與前期的比較"""
        
        total_records = db.session.query(func.count(Sample.id)).scalar()
        
        if total_records < 2:
            return { 'total_records': total_records, 'avg_metric_a': 0, 'avg_metric_b': 0, 'latest_record_time': None, 'prev_avg_metric_a': 0, 'prev_avg_metric_b': 0 }

        # --- 原有計算 (不變) ---
        avg_metric_a = db.session.query(func.avg(Sample.metric_a)).scalar()
        avg_metric_b = db.session.query(func.avg(Sample.metric_b)).scalar()
        latest_record_time = db.session.query(func.max(Sample.timestamp)).scalar()
        
        # --- 修正後的計算邏輯 ---
        latest_record = Sample.query.order_by(Sample.timestamp.desc()).first()
        
        # 直接在新的查詢中，加入 filter 條件來排除最新一筆紀錄
        prev_avg_metric_a = db.session.query(func.avg(Sample.metric_a)).filter(Sample.id != latest_record.id).scalar()
        prev_avg_metric_b = db.session.query(func.avg(Sample.metric_b)).filter(Sample.id != latest_record.id).scalar()

        # --- 組合回傳資料 (不變) ---
        return {
            'total_records': total_records,
            'avg_metric_a': round(avg_metric_a, 2) if avg_metric_a else 0,
            'avg_metric_b': round(avg_metric_b, 2) if avg_metric_b else 0,
            'latest_record_time': latest_record_time.isoformat() if latest_record_time else None,
            'prev_avg_metric_a': round(prev_avg_metric_a, 2) if prev_avg_metric_a else 0,
            'prev_avg_metric_b': round(prev_avg_metric_b, 2) if prev_avg_metric_b else 0,
        }