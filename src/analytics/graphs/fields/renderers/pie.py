# 円グラフの描画
from __future__ import annotations
from ..plot_data import PlotData
from ...types import VerticalAxis

class PieRenderer:
    def render(self, ax, data: PlotData, *, verticalAxis: VerticalAxis) -> None:
        def format_value(pct: float, allvalues: list[float]) -> str:
            total = sum(allvalues)
            value = pct / 100.0 * total
            if verticalAxis == 'time':
                return f'{value:.2f}時間'
            return f'{value:.2f}%'
        
        ax.pie(
            x=list(data.values),
            labels=list(data.labels),
            colors=list(data.colors),
            counterclock=False,
            startangle=90,
            autopct=lambda pct: format_value(pct, list(data.values)),
        )
        ax.axis('equal')
        ax.legend(loc='upper left', bbox_to_anchor=(0.8, 1), edgecolor='black', borderaxespad=0)
