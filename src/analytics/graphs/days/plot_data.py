# Plotデータの生成ファイル
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from ..types import VerticalAxis

@dataclass(frozen=True)
class PlotData:
    labels: list[str]
    values: dict[str, list[float]]
    colors: dict[str, str]

def build_plot_data(logs: Sequence[tuple[str, str, str, float | None]], *, verticalAxis: VerticalAxis) -> PlotData:
    # x
    labels = sorted(list(set(selected_date for selected_date, _, _, _ in logs)))
    # height
    date_len = len(labels)
    fieldnames = sorted({fieldname for _, fieldname, _, _ in logs})
    values = {f: [0.0] * date_len for f in fieldnames}
    
    # color
    colors = {fieldname: color for _, fieldname, color, _ in logs}

    return PlotData(labels=labels, values=values, colors=colors)

