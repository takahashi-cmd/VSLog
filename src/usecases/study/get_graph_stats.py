from datetime import date
from dataclasses import dataclass

from ...analytics.periods import study_periods
from ...analytics.graphs.days.service import make_graph_by_days
from ...analytics.graphs.fields.service import make_graph_by_fields
from ...analytics.db.aggregate import agg_by_fields, agg_by_days
from ...analytics.db.metrics import sum_hours_and_days, total_day as total_day_all, total_hour as total_hour_all
from ...analytics.stats.study_stats import build_stats

@dataclass(frozen=True)
class GraphStatsResult:
    svg: str
    total_day: int
    total_hour: float
    avg_hour: float

@dataclass(frozen=True)
class StatsResult:
    total_day: int
    total_hour: float
    avg_hour:float

def _get_stats(user_id: str, period: str, first_day: date | None = None, last_day: date | None = None) -> StatsResult:
    if period == 'all':
        total_hours = total_hour_all(user_id)
        study_days = total_day_all(user_id)
    else:
        if first_day is None or last_day is None:
            raise ValueError("first_day/last_day is required unless period == 'all'")
        total_hours, study_days = sum_hours_and_days(user_id, first_day, last_day)

    s = build_stats(total_hours, study_days)
    return StatsResult(s['total_day'], s['total_hour'], s['avg_hour'])

# グラフ、統計値の取得
def get_graph_stats_usecase(
    *,
    user_id: str,
    period: str | None,
    year: int | None,
    month_year: str | None,
    month: int | None,
    horizontalAxis: str | None,
    verticalAxis: str | None,
    graphType: str | None,
    ) -> GraphStatsResult:
    '''
    1) first_day, last_dayを決める
    2) logsを取得
    3) svg, statsを返す
    '''

    # 1) first_day, last_day
    first_day = last_day = None
    month_num = None

    if period == 'this_week':
        today = date.today()
        first_day, last_day = study_periods.this_week(today)
    
    elif period == 'last_week':
        today = date.today()
        first_day, last_day = study_periods.last_week(today)
    
    elif period == 'month':
        first_day, last_day, month_num = study_periods.month_range(month_year, month)
    
    elif period == 'year':
        first_day, last_day = study_periods.year_range(year)
    
    elif period == 'all':
        pass

    else:
        raise ValueError(f"invalid period: {period}")
    
    # 2, 3) logs, svg, stats
    if horizontalAxis == 'days':
        logs = agg_by_days(user_id, first_day=first_day, last_day=last_day)
        svg = make_graph_by_days(
            logs=logs,
            period=period,
            verticalAxis=verticalAxis,
            graphType=graphType,
            first_day=first_day,
            last_day=last_day,
            year=year,
            month=month,
            month_num=month_num,
            )

        stats = _get_stats(user_id, period, first_day, last_day)
        return GraphStatsResult(svg=svg, total_day=stats.total_day, total_hour=stats.total_hour, avg_hour=stats.avg_hour)

    elif horizontalAxis == 'fields':
        logs = agg_by_fields(user_id, first_day=first_day, last_day=last_day)
        svg = make_graph_by_fields(
            logs=logs,
            period=period,
            verticalAxis=verticalAxis,
            graphType=graphType,
            first_day=first_day,
            last_day=last_day,
            year=year,
            month=month,
            month_num=month_num,
            )

        stats = _get_stats(user_id, period, first_day, last_day)
        return GraphStatsResult(svg=svg, total_day=stats.total_day, total_hour=stats.total_hour, avg_hour=stats.avg_hour)

    raise ValueError(f"invalid horizontalAxis: {horizontalAxis}")
