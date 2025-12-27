# 共通型定義
from typing import Literal

# グラフ種類
GraphType = Literal['bar', 'pie', 'line']

# 横軸表示形式
HorizontalAxis = Literal['days', 'fields']

# 縦軸表示形式
VerticalAxis = Literal['time', 'percent']

# 期間
Period = Literal['this_week', 'last_week', 'month', 'year', 'all']
