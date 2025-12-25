# 棒グラフの描画
from __future__ import annotations
import matplotlib.pyplot as plt
from ..data import PlotData
from ...types import VerticalAxis

class BarRenderer:
    def render(self, ax, data: PlotData, *, verticalAxis: VerticalAxis) -> None:
        ax.bar(data.labels, data.values, color=data.colors)
        ax.grid(True)
        ax.set_xlabel('学習分野')
        ax.set_ylabel('学習時間（時間）' if verticalAxis == 'time' else '学習時間（%）')

        ymax_val = max(data.values) if data.values else 0
        padding = max(1, ymax_val * 0.1)
        ax.set_ylim(0, ymax_val + padding)

        plt.setp(ax.get_xticklabels(), rotation=45, ha='center')
        for x, y in zip(data.labels, data.values):
            plt.text(x, y, f'{y:.2f}', ha='center', va='bottom')
        
        ax.legend(loc='upper left', bbox_to_anchor=(1.04, 1), edgecolor='black', borderaxespad=0)

