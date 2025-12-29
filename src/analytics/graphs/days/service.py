#  グラフを描画するためのロジックファイル
from __future__ import annotations
import matplotlib.pyplot as plt
from typing import Sequence

from ..mpl_config import configure_matplotlib
from .plot_data import build_plot_data
from ..types import VerticalAxis, GraphType
from ..title import TitleContext, make_title
from ..svg import fig_to_svg_base64


def make_graph_by_days(
    *,
    logs: Sequence[tuple[str, str, str, float | None]],
    period: str,
    verticalAxis: VerticalAxis,
    graphType: GraphType,
    first_day=None,
    last_day=None,
    year=None,
    month=None,
    month_num=None,
    ):
    """
    logs: agg_by_days の結果
      (selected_date, fieldname, color_code, total_hour)
    """

    # 1.matplotlibの設定ファイルの読み込み
    configure_matplotlib()

    # 2.プロットデータの生成
    if not logs:
        return None
    
    plot_data = build_plot_data(logs, verticalAxis=verticalAxis)

    # 3.グラフ描画の初期設定（fig, axの準備）
    fig, ax = plt.subplots(figsize(10, 4))

    # 4.グラフ種類に応じたグラフ描画
    renderer = get_renderer(graphType)
    renderer.render(ax, plot_data, verticalAxis=verticalAxis)

    # 5.グラルタイトルの生成
    title = make_title(
        TitleContext(
            period=period,
            first_day=first_day,
            last_day=last_day,
            year=year,
            month=month,
            month_num=month_num,
        )
    )
    if title:
        ax.set_title(title, y=1.04)

    # 6.svgへの出力
    svg_b64 = fig_to_svg_base64(fig)
    plt.close(fig)

    return svg_b64