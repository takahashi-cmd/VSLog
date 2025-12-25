# グラフ描画のエントリーポイント
from __future__ import annotations
from ...types import GraphType
from .bar import BarRenderer
from .pie import PieRenderer
from .base import FieldsRenderer

def get_renderer(graphType: GraphType) -> FieldsRenderer:
    if graphType == 'bar':
        return BarRenderer()
    if graphType == 'pie':
        return PieRenderer
    raise ValueError(f'invalid graphType: {graphType}')
