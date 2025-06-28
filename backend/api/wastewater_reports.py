# backend/api/wastewater_reports.py

from flask_restx import Namespace, Resource, fields
from models import WastewaterReport # 匯入我們的兩個新模型
from extensions import db

# 建立一個新的 Namespace
ns = Namespace('wastewater-reports', description='廢水報告相關操作')

# 建立給「檢測項目」用的輸出模型
report_item_model = ns.model('WastewaterReportItem', {
    'id': fields.Integer(readonly=True),
    'item_name': fields.String(required=True),
    'value': fields.Float(required=True),
    'unit': fields.String,
    'standard': fields.String,
    'is_compliant': fields.Boolean,
})

# 建立給「廢水報告主體」用的輸出模型
# 這是這次的重點：我們會在報告模型中，巢狀地引用「檢測項目模型」
report_model = ns.model('WastewaterReport', {
    'id': fields.Integer(readonly=True),
    'report_date': fields.DateTime(dt_format='iso8601'),
    'vendor': fields.String(required=True),
    'status': fields.String,
    # 使用 fields.List 和 fields.Nested 來處理「一對多」的關聯資料
    'items': fields.List(fields.Nested(report_item_model))
})

# 建立獲取列表的 Resource
report_parser = ns.parser()
report_parser.add_argument('status', type=str, help='依狀態篩選報告')
report_parser.add_argument('search', type=str, help='依廠商名稱關鍵字搜尋')

@ns.route('/')
class WastewaterReportList(Resource):
    
    @ns.marshal_list_with(report_model)
    @ns.expect(report_parser)
    def get(self):
        """獲取所有廢水報告列表 (支援狀態篩選與廠商搜尋)"""
        args = report_parser.parse_args()
        status_filter = args['status']
        search_term = args['search'] # <-- 取得搜尋關鍵字

        base_query = WastewaterReport.query

        if status_filter and status_filter.lower() != '全部':
            base_query = base_query.filter(WastewaterReport.status == status_filter)
        
        # 如果有提供搜尋關鍵字，則加入 like 篩選條件
        if search_term:
            # .like(f"%{search_term}%") 可以做到模糊比對 (contains)
            base_query = base_query.filter(WastewaterReport.vendor.like(f"%{search_term}%"))
            
        reports = base_query.order_by(WastewaterReport.report_date.desc()).all()
        return reports