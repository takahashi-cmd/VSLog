# 分野別学習グラフの作成
from __future__ import annotations
import platform
from typing import Literal
import matplotlib.pyplot as plt
from .mpl_config import configure_matplotlib
from .svg import fig_to_svg_base64

GraphType = Literal['bar', 'pie']
VerticalAxis = Literal['time', 'percent']

def _date_format(fmt_windows: str, fmt_unix: str) -> str:
    return fmt_windows if platform.system() == "Windows" else fmt_unix

def make_graph_by_fields(*,
logs,
period: str,
verticalAxis: VerticalAxis,
graphType: GraphType,
first_day=None,
last_day=None,
year=None,
month=None,
month_num=None,
):
    configure_matplotlib()

    if not logs:
        return None
    
    if verticalAxis == 'time':
        data = {fieldname: float(hour or 0.0) for fieldname, _, hour in logs}
    else:
        total_all = sum(float(hour or 0.0) for _, _, hour in logs) or 1.0
        data = {fieldname: round((float(hour or 0.0) / total_all * 100.0), 1) for fieldname, _, hour in logs}
    color_map = {fieldname: color_code for fieldname, color_code, _ in logs}

    fig, ax = plt.subplots(figsize=(10, 4))

    if graphType == 'bar':
        ax.bar(data.keys(), data.values(), color=[color_map[f] for f in data.keys()])
        ax.grid(True)
        ax.set_xlabel('学習分野')
        ax.set_ylabel('学習時間（時間）' if verticalAxis == 'time' else '学習時間（%）')

        ymax_val = max(data.values()) if data else 0
        padding = max(1, ymax_val * 0.1)
        ax.set_ylim(0, ymax_val + padding)

        plt.setp(ax.get_xticklabels(), rotation=45, ha='center')
        for x, y in zip(data.keys(), data.values()):
            plt.text(x, y, f'{y:.2f}', ha='center', va='bottom')
    
    elif graphType == 'pie':
        def format_value(pct, allvalues):
            total = sum(allvalues)
            value = pct / 100 * total
            if verticalAxis == 'time':
                return f'{value:.2f}時間'
            return f'{value:.2f}%'
        
        ax.pie(
            x=list(data.values()),
            labels=list(data.keys()),
            colors=[color_map[f] for f in data.keys()],
            counterclock=False,
            startangle=90,
            autopct=lambda pct: format_value(pct, list(data.values()))
        )
        ax.axis('equal')
        ax.legend(loc='upper left', bbox_to_anchor=(0.8, 1), edgecolor='black', borderaxespad=0)
    else:
        raise ValueError(f'invalid graphType: {graphType}')
    
    # タイトル
    date_format = _date_format('%#m/%#d(%a)', '%-m/%-d(%a)')
    if period in ('this_week', 'last_week'):
        ax.set_title(f'{first_day.strftime(date_format)}～{last_day.strftime(date_format)}の学習履歴', y=1.04)
    elif period == 'month' and year and month and month_num:
        ax.set_title(f'{year}年{month}月1日～{month}月{month_num}日の分野別学習履歴', y=1.04)
    elif period == 'year' and year:
        ax.set_title(f'{year}年の分野別学習履歴', y=1.04)
    elif period == 'all':
        ax.set_title('分野別全期間の学習履歴', y=1.04)
    
    svg_b64 = fig_to_svg_base64(fig)
    plt.close(fig)
    return svg_b64
