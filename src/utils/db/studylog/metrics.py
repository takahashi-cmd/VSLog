# StudyLogメトリクス用のクエリ
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import func

from ....extensions import db
from ....models import StudyLog

def _build_filters(user_id: str, first_day: date | None = None, last_day: date | None = None):
    filters = [StudyLog.user_id == user_id]
    if first_day:
        filters.append(StudyLog.study_date >= first_day)
    if last_day:
        filters.append(StudyLog.study_date <= last_day)
    return filters

# 期間に応じた学習時間の合計、学習日数の取得
def sum_hours_and_days(user_id: str, first_day: date, last_day: date) -> tuple[float, int]:
    filters = _build_filters(user_id, first_day, last_day)
    total_hours = (
        db.session.query(func.sum(StudyLog.hour))
        .filter(*filters)
        .scalar()
    )

    study_days = (
        db.session.query(func.count(func.distinct(StudyLog.study_date)))
        .filter(*filters)
        .scalar()
    )

    return float(total_hours or 0.0), int(study_days or 0)

# 全学習日数の取得
def total_day(user_id: str) -> int:
    v = db.session.query(func.count(func.distinct(StudyLog.study_date))).filter_by(user_id=user_id).scalar()
    return int(v or 0)

# 全学習時間の取得
def total_hour(user_id: str) -> float:
    v = db.session.query(func.sum(StudyLog.hour)).filter_by(user_id=user_id).scalar()
    return float(v or 0.0)
