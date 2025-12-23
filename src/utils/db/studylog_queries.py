# DB検索、集計クエリ
from __future__ import annotations

from datetime import date, datetime
from typing import Optional, Sequence

from sqlalchemy import func
from sqlalchemy.sql import label

from ...extensions import db
from ...models import Field
from ...models import StudyLog

# ユーザー毎の全学習履歴取得
def get_study_logs_all(user_id: str):
    return StudyLog.query.filter_by(user_id=user_id).all()

# 学習日に応じたユーザー毎の学習履歴取得
def get_study_logs_by_study_date(user_id: str, date_str: str):
    study_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    logs = (
        db.session.query(StudyLog.study_log_id, StudyLog.study_date, Field.fieldname.label('fieldname'), StudyLog.content, StudyLog.hour)
        .join(Field, StudyLog.field_id == Field.field_id)
        .filter(
        StudyLog.user_id == user_id,
        StudyLog.study_date == date_str
        )
        .all()
    )

    if not logs:
        return None
    
    return logs

# 月に応じたユーザー毎の学習履歴取得
def get_study_logs_by_study_month(user_id: str, first_day: date, last_day: date):
    logs = (
        db.session.query(StudyLog.study_log_id, StudyLog.study_date, Field.fieldname.label('fieldname'), StudyLog.content, StudyLog.hour)
        .join(Field, StudyLog.field_id == Field.field_id)
        .filter(
        StudyLog.user_id == user_id,
        StudyLog.study_date >= first_day,
        StudyLog.study_date <= last_day
        )
        .all()
    )
    return logs

# 期間に応じた学習時間の合計、学習日数の取得
def sum_hours_and_days(user_id: str, first_day: date, last_day: date):
    total_hours = (
        db.session.query(func.sum(StudyLog.hour))
        .filter(
            StudyLog.user_id == user_id,
            StudyLog.study_date >= first_day,
            StudyLog.study_date <= last_day
        )
        .scalar()
    )

    study_days = (
        db.session.query(func.count(func.distinct(StudyLog.study_date)))
        .filter(
            StudyLog.user_id == user_id,
            StudyLog.study_date >= first_day,
            StudyLog.study_date <= last_day
        )
        .scalar()
    )

    return total_hours, study_days

# 全学習日数の取得
def total_day(user_id: str) -> int:
    v = db.session.query(func.count(func.distinct(StudyLog.study_date))).filter_by(user_id=user_id).scalar()
    return int(v or 0)

# 全学習時間の取得
def total_hour(user_id: str) -> float:
    v = db.session.query(func.sum(StudyLog.hour)).filter_by(user_id=user_id).scalar()
    return float(v or 0.0)


# 横軸表示形式「年月日」の集計
def agg_by_days(user_id: str, *, period: str, first_day: date | None = None, last_day: date | None = None):
    if period in ('this_week', 'last_week', 'month'):
        selected_date = StudyLog.study_date
    elif period == 'year':
        selected_date = func.date_format(StudyLog.study_date, '%m').label('month')
    elif period == 'all':
        selected_date = func.date_format(StudyLog.study_date, '%Y').label('year')
    else:
        raise ValueError(f'invalid period: {period}')
    
    filters = [StudyLog.user_id == user_id]
    if first_day:
        filters.append(StudyLog.study_date >= first_day)
    if last_day:
        filters.append(StudyLog.study_date <= last_day)

    logs = (
        db.session.query(selected_date, Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(StudyLog.hour).label('total_hour'))
        .join(Field, StudyLog.field_id == Field.field_id)
        .filter(*filters)
        .group_by(selected_date, Field.fieldname, Field.color_code)
        .all()
    )

    if not logs:
        return None
    
    return logs


# 横軸表示形式「分野別」の集計
def agg_by_fields(user_id: str, *, first_day: date | None = None, last_day: date | None = None):
    filters = [StudyLog.user_id == user_id]
    if first_day:
        filters.append(StudyLog.study_date >= first_day)
    if last_day:
        filters.append(StudyLog.study_date <= last_day)

    logs = (
    db.session.query(Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(StudyLog.hour).label('total_hour'))
    .join(Field, StudyLog.field_id == Field.field_id)
    .filter(*filters)
    .group_by(Field.fieldname, Field.color_code)
    .order_by(func.sum(StudyLog.hour).desc())
    .all()
)

    if not logs:
        return None
    
    return logs
