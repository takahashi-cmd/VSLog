# 今週/先週/月/年の期間計算
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
import calendar

@dataclass(frozen=True)
class PeriodRange:
    first_day: date
    last_day: date

def this_week(today: date | None = None) -> PeriodRange:
    today = today or date.today()
    first = today - timedelta(days=today.weekday())
    last = first + timedelta(days=6)
    return PeriodRange(first, last)

def last_week(today: date | None = None) -> PeriodRange:
    today = today or date.today()
    first = today -timedelta(days=today.weekday() + 7)
    last = first + timedelta(days=6)
    return PeriodRange(first, last)

def month_range(month_year: int, month: int) -> tuple[PeriodRange, int]:
    first = date(month_year, month, 1)
    month_num = calendar.monthrange(month_year, month)[1]
    last = date(month_year, month, month_num)
    return PeriodRange(first, last), month_num # 月日数は期間ではないので、PeriodRangeに混ぜない

def year_range(year: int) -> PeriodRange:
    first = date(year, 1, 1)
    last = date(year, 12, 31)
    return PeriodRange(first, last)
