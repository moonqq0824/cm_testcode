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

# 建立一個請求解析器，用來處理 URL 查詢參數
parser = ns.parser()
parser.add_argument('page', type=int, default=1, help='頁碼')
parser.add_argument('per_page', type=int, default=5, help='每頁筆數')


@ns.route('/')
class SampleList(Resource):
    
    @ns.marshal_with(sample_list_model)
    @ns.expect(parser) # 告訴 Swagger UI 我們期望接收這些參數
    def get(self):
        """獲取產線紀錄列表 (支援分頁)"""
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        
        # 使用 SQLAlchemy 的 paginate() 方法進行分頁查詢
        # error_out=False 能防止在請求不存在的頁面時拋出 404 錯誤
        pagination_obj = Sample.query.order_by(Sample.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # 從分頁物件中提取我們需要的資料
        paginated_samples = pagination_obj.items
        
        response_data = {
            'data': paginated_samples,
            'pagination': {
                'total_items': pagination_obj.total,
                'total_pages': pagination_obj.pages,
                'current_page': pagination_obj.page,
                'per_page': pagination_obj.per_page,
                'has_next': pagination_obj.has_next,
                'has_prev': pagination_obj.has_prev
            }
        }
        
        return response_data, 200