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
    
class WastewaterReport(db.Model):
    """廢水報告模型 (一)"""
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    vendor = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='合格') # 例如: 合格, 部分項目不合格, 追蹤中

    # 建立「一對多」的關聯，'items' 屬性可以讓我們存取所有關聯的檢測項目
    # backref='report' 讓每個檢測項目物件都能透過 .report 屬性反向找到它所屬的報告
    # cascade='all, delete-orphan' 確保在刪除一份報告時，其下所有關聯的檢測項目也會被一併刪除
    items = db.relationship('WastewaterReportItem', backref='report', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<WastewaterReport id={self.id} vendor={self.vendor}>'


class WastewaterReportItem(db.Model):
    """廢水報告的檢測項目模型 (多)"""
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50))
    standard = db.Column(db.String(50))
    is_compliant = db.Column(db.Boolean, default=True)

    # 建立「外鍵 (Foreign Key)」，指向 wastewater_report 表格的 id 欄位
    # 這是「多」這一端，用來記錄自己屬於「哪一筆」報告
    report_id = db.Column(db.Integer, db.ForeignKey('wastewater_report.id'), nullable=False)

    def __repr__(self):
        return f'<WastewaterReportItem id={self.id} item_name={self.item_name}>'
