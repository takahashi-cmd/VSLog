# Plotデータの生成ファイル
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from ..types import VerticalAxis

@dataclass(frozen=True)
class PlotData:
    labels: list[str]
    values: list[float]
    colors: list[str]

def build_plot_data(logs: Sequence[tuple[str, str, float | None]], *, verticalAxis: VerticalAxis,) -> PlotData:
    labels = [fieldname for fieldname, _, _ in logs]
    raw_hours = [float(hour or 0.0) for _, _, hour in logs]
    colors = [color_code for _, color_code, _ in logs]

    if verticalAxis == 'time':
        values = raw_hours
    else:
        total_all = sum(raw_hours) or 1.0
        values = [round((h / total_all * 100.0), 1) for h in raw_hours]
    
    return PlotData(labels=labels, values=values, colors=colors)

