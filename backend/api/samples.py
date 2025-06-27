# backend/api/samples.py (全新內容)

from flask_restx import Namespace, Resource, fields
from models import Sample # 從 models.py 匯入我們的 Sample 模型

# 1. 建立一個新的 Namespace，專門給 sample 功能使用
ns = Namespace('samples', description='產線紀錄相關操作')

# 2. 定義 API 的輸出模型 (Marshalling 的藍圖)
#    這會告訴 RESTx 如何將 Sample 物件序列化為 JSON
sample_model = ns.model('SampleModel', {
    'id': fields.Integer(readonly=True, description='紀錄的唯一識別碼'),
    'line_name': fields.String(required=True, description='產線名稱'),
    'product_name': fields.String(description='產品名稱'),
    'timestamp': fields.DateTime(dt_format='iso8601', description='紀錄時間'),
    'metric_a': fields.Float(description='指標 A'),
    'metric_b': fields.Float(description='指標 B'),
    'operator': fields.String(description='操作員')
})

# 3. 定義列表的完整輸出模型 (包含分頁資訊)
#    我們暫時先回傳假的分頁資訊
pagination_model = ns.model('PaginationModel', {
    'total_items': fields.Integer(default=0),
    'total_pages': fields.Integer(default=0),
    'current_page': fields.Integer(default=1),
    'per_page': fields.Integer(default=20),
    'has_next': fields.Boolean(default=False),
    'has_prev': fields.Boolean(default=False)
})

sample_list_model = ns.model('SampleListModel', {
    'data': fields.List(fields.Nested(sample_model)),
    'pagination': fields.Nested(pagination_model)
})

# 4. 改造 Resource
@ns.route('/') # 將路由註冊到這個 namespace 下
class SampleList(Resource):
    
    @ns.marshal_with(sample_list_model) # 使用我們定義的列表模型來封送回傳值
    def get(self):
        """獲取產線紀錄列表"""
        
        # 從資料庫查詢所有 Sample 紀錄
        all_samples = Sample.query.all()
        
        # 組合回傳的資料結構，以符合 sample_list_model 的定義
        # TODO: 未來這裡會加上真正的分頁邏輯
        response_data = {
            'data': all_samples,
            'pagination': {
                'total_items': len(all_samples),
                'total_pages': 1,
                'current_page': 1,
                'per_page': len(all_samples),
                'has_next': False,
                'has_prev': False
            }
        }
        
        return response_data, 200