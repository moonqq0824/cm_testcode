# backend/api/wastewater_reports.py

from flask_restx import Namespace, Resource, fields
from models import WastewaterReport, WastewaterReportItem
from extensions import db
from datetime import datetime

# --- Namespace and Parsers ---
ns = Namespace('wastewater-reports', description='廢水報告相關操作')
report_parser = ns.parser()
report_parser.add_argument('status', type=str, help='依狀態篩選報告')
report_parser.add_argument('search', type=str, help='依廠商名稱關鍵字搜尋')

# --- Output Models (For GET requests) ---
report_item_model = ns.model('WastewaterReportItem', {
    'id': fields.Integer(readonly=True),
    'item_name': fields.String(required=True),
    'value': fields.Float(required=True),
    'unit': fields.String,
    'standard': fields.String,
    'is_compliant': fields.Boolean,
})
report_model = ns.model('WastewaterReport', {
    'id': fields.Integer(readonly=True),
    'report_date': fields.DateTime(dt_format='iso8601'),
    'vendor': fields.String(required=True),
    'status': fields.String,
    'items': fields.List(fields.Nested(report_item_model))
})

# --- Input Models (For POST requests) ---
report_item_input_model = ns.model('WastewaterReportItemInput', {
    'item_name': fields.String(required=True, description='項目名稱'),
    'value': fields.Float(required=True, description='檢測值'),
    'unit': fields.String(description='單位'),
    'standard': fields.String(description='標準值'),
    'is_compliant': fields.Boolean(required=True, description='是否合格'),
})
report_input_model = ns.model('WastewaterReportInput', {
    'vendor': fields.String(required=True, description='廠商名稱'),
    'status': fields.String(required=True, description='總體狀態'),
    'report_date': fields.Date(required=True, description='報告日期 (YYYY-MM-DD)'),
    'items': fields.List(fields.Nested(report_item_input_model), required=True, description='檢測項目列表')
})

# --- API Resources ---
@ns.route('/')
class WastewaterReportList(Resource):
    
    @ns.marshal_list_with(report_model)
    @ns.expect(report_parser)
    def get(self):
        """獲取所有廢水報告列表 (支援狀態篩選與廠商搜尋)"""
        args = report_parser.parse_args()
        status_filter = args.get('status')
        search_term = args.get('search')

        base_query = WastewaterReport.query

        if status_filter and status_filter.lower() != '全部':
            base_query = base_query.filter(WastewaterReport.status == status_filter)
        
        if search_term:
            base_query = base_query.filter(WastewaterReport.vendor.like(f"%{search_term}%"))
            
        reports = base_query.order_by(WastewaterReport.report_date.desc()).all()
        return reports

    @ns.expect(report_input_model, validate=True)
    @ns.marshal_with(report_model, code=201)
    def post(self):
        """新增一筆完整的廢水報告"""
        data = ns.payload
        
        new_report = WastewaterReport(
            vendor=data['vendor'],
            status=data['status'],
            report_date=datetime.strptime(data['report_date'], '%Y-%m-%d').date()
        )
        
        # 建立關聯的檢測項目
        if 'items' in data and data['items']:
            for item_data in data['items']:
                new_item = WastewaterReportItem(
                    item_name=item_data['item_name'],
                    value=item_data['value'],
                    unit=item_data.get('unit'),
                    standard=item_data.get('standard'),
                    is_compliant=item_data['is_compliant'],
                    report=new_report
                )
                db.session.add(new_item)
        
        db.session.add(new_report)
        db.session.commit()
        
        return new_report, 201