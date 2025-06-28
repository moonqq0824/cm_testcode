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

# 更新請求解析器，加入排序相關參數
parser = ns.parser()
parser.add_argument('page', type=int, default=1, help='頁碼')
parser.add_argument('per_page', type=int, default=5, help='每頁筆數')
parser.add_argument('sort_by', type=str, default='timestamp', help='排序欄位')
parser.add_argument('order', type=str, default='desc', help='排序順序 (asc/desc)')
parser.add_argument('line_name', type=str, help='產線名稱篩選') # <-- 新增篩選參數


@ns.route('/')
class SampleList(Resource):
    
    @ns.marshal_with(sample_list_model)
    @ns.expect(parser)
    def get(self):
        """獲取產線紀錄列表 (支援分頁、排序與篩選)"""
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        sort_by_column_name = args['sort_by']
        order_direction = args['order']
        line_name_filter = args['line_name'] # <-- 取得篩選參數值

        # 基礎查詢
        base_query = Sample.query

        # 如果有提供產線名稱篩選，則加入 filter 條件
        if line_name_filter:
            base_query = base_query.filter(Sample.line_name == line_name_filter)
            
        # 動態排序邏輯
        sort_column = getattr(Sample, sort_by_column_name, Sample.timestamp)
        
        if order_direction.lower() == 'asc':
            order_logic = sort_column.asc()
        else:
            order_logic = sort_column.desc()
            
        # 將排序與分頁應用到查詢中
        pagination_obj = base_query.order_by(order_logic).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        paginated_samples = pagination_obj.items
        
        response_data = {
            'data': paginated_samples,
            'pagination': {
                'total_items': pagination_obj.total,
                # ... 其他分頁欄位不變 ...
                'total_pages': pagination_obj.pages,
                'current_page': pagination_obj.page,
                'per_page': pagination_obj.per_page,
                'has_next': pagination_obj.has_next,
                'has_prev': pagination_obj.has_prev
            }
        }
        
        return response_data, 200
    @ns.doc(body=ns.model('BatchDeleteInput', {
        'ids': fields.List(fields.Integer, required=True, description='要刪除的紀錄 ID 列表')
    }))
    def delete(self):
        """批次刪除多筆產線紀錄"""
        # ns.payload 會自動解析請求 body 中的 JSON 資料
        ids_to_delete = ns.payload.get('ids')

        if not ids_to_delete:
            # 如果沒有提供 ids，回傳一個錯誤請求
            return {'message': '請提供要刪除的 ID 列表'}, 400

        # 使用 SQLAlchemy 的 in_ 運算子來一次刪除所有對應的紀錄
        num_deleted = db.session.query(Sample).filter(Sample.id.in_(ids_to_delete)).delete(synchronize_session=False)
        db.session.commit()

        if num_deleted > 0:
            return {'message': f'成功刪除 {num_deleted} 筆紀錄'}, 200
        else:
            return {'message': '找不到對應的紀錄可供刪除'}, 404
