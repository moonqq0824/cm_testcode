# backend/api/charts.py

from flask_restx import Namespace, Resource
from collections import defaultdict
from models import Sample

ns = Namespace('charts', description='圖表數據相關操作')

@ns.route('/line-comparison')
class LineComparisonChart(Resource):
    def get(self):
        """提供產線交叉比對的折線圖數據"""
        
        # 為了示範，我們先抓取最新的 30 筆資料
        records = Sample.query.order_by(Sample.timestamp.desc()).limit(30).all()
        records.reverse() # 將資料反轉，讓時間從左到右遞增

        if not records:
            return {'labels': [], 'datasets': []}

        # --- 資料轉換 ---
        # 我們需要將資料從 [row1, row2, ...] 的格式，轉換成 Chart.js 需要的格式
        
        labels = [] # X 軸的標籤 (時間)
        
        # 用一個字典來按產線分組數據
        # defaultdict 讓我們在key不存在時，能自動建立一個空列表
        data_by_line = defaultdict(list)

        for record in records:
            # 格式化時間作為 X 軸標籤
            label = record.timestamp.strftime('%H:%M:%S')
            labels.append(label)
            
            # 將各產線的指標A數據分別存起來
            # 這裡我們假設所有產線在每個時間點都有數據，實際情況可能更複雜
            data_by_line[record.line_name].append(record.metric_a)

        # 定義每條線的顏色
        colors = {
            '產線A': 'rgba(255, 99, 132, 1)',
            '產線B': 'rgba(54, 162, 235, 1)',
            '產線C': 'rgba(75, 192, 192, 1)',
        }

        # 組合 Chart.js 需要的 datasets 格式
        datasets = []
        for line_name, data_points in data_by_line.items():
            color = colors.get(line_name, 'rgba(201, 203, 207, 1)') # 如果產線沒有預設顏色，給一個灰色
            datasets.append({
                'label': line_name,
                'data': data_points,
                'borderColor': color,
                'backgroundColor': color.replace('1)', '0.5)'), # 將顏色變為半透明作為背景色
                'tension': 0.1
            })

        return {
            'labels': labels,
            'datasets': datasets,
        }