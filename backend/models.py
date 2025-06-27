# backend/models.py

from extensions import db
from datetime import datetime

class Sample(db.Model):
    """產線紀錄模型"""
    
    # __tablename__ = 'samples' # 可選：明確指定資料表名稱

    # 定義資料表欄位
    id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    metric_a = db.Column(db.Float, nullable=True)
    metric_b = db.Column(db.Float, nullable=True)
    operator = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """定義物件的文字表示法，方便除錯"""
        return f'<Sample id={self.id} line_name={self.line_name}>'