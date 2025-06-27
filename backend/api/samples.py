# backend/api/samples.py

from flask_restx import Resource

# 這是我們在 API 規格中定義的假資料
MOCK_DATA = {
    "data": [
        {
            "id": 101,
            "line_name": "產線A",
            "product_name": "產品X",
            "timestamp": "2025-06-27T14:30:00Z",
            "metric_a": 15.2,
            "metric_b": 88.9,
            "operator": "張三"
        },
        {
            "id": 102,
            "line_name": "產線A",
            "product_name": "產品Y",
            "timestamp": "2025-06-27T14:35:00Z",
            "metric_a": 15.5,
            "metric_b": 89.1,
            "operator": "李四"
        }
    ],
    "pagination": {
        "total_items": 153,
        "total_pages": 8,
        "current_page": 1,
        "per_page": 20,
        "has_next": True,
        "has_prev": False
    }
}

class SampleList(Resource):
    def get(self):
        """獲取產線紀錄列表"""
        # 現在我們先直接回傳固定的假資料
        return MOCK_DATA, 200