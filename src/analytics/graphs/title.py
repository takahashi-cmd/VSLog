# グラフタイトルの設定ファイル
from __future__ import annotations
import platform
from dataclasses import dataclass
from datetime import date
from typing import Callable
from .types import Period

def _date_format(fmt_windows: str, fmt_unix: str) -> str:
    return fmt_windows if platform.system() == 'Windows' else fmt_unix

@dataclass(frozen=True)
class TitleContext:
    period: Period
    first_day: date | None = None
    last_day : date | None = None
    year: int | None = None
    month: int | None = None
    month_num: int | None = None

# periodに応じてタイトルを生成する関数
def _week_title(ctx: TitleContext, date_fmt: str) -> str | None:
    if not (ctx.first_day and ctx.last_day):
        return None
    return f'{ctx.first_day.strftime(date_fmt)}～{ctx.last_day.strftime(date_fmt)}'

def _month_title(ctx: TitleContext, date_fmt: str) -> str | None:
    if not (ctx.year and ctx.month and ctx.month_num):
        return None
    return f'{ctx.year}年{ctx.month}月1日～{ctx.month}月{ctx.month_num}日の学習履歴'

def _year_title(ctx: TitleContext, date_fmt: str) -> str | None:
    if not ctx.year:
        return None
    return f'{ctx.year}年の学習履歴'

def _all_title(ctx: TitleContext, date_fmt: str) -> str | None:
    return '全期間の学習履歴'

# period -> builder の対応表
_BUILDER_BY_PERIOD: dict[Period, Callable[[TitleContext, str], str | None]] = {
    'this_week': _week_title,
    'last_week': _week_title,
    'month': _month_title,
    'year': _year_title,
    'all': _all_title,
}

def make_title(ctx: TitleContext) -> str | None:
    date_fmt = _date_format('%#m/%#d(%a)', '%-m/%-d(%a)')
    builder = _BUILDER_BY_PERIOD.get(ctx.period)
    if builder is None:
        return None
    return builder(ctx, date_fmt)
