# StudyLog集計用のクエリ
from __future__ import annotations

from datetime import date

from sqlalchemy import func

from ....extensions import db
from ....models import Field
from ....models import StudyLog

# 共通のフィルター条件
def _build_filters(user_id: str, first_day: date | None = None, last_day: date | None = None):
    filters = [StudyLog.user_id == user_id]
    if first_day:
        filters.append(StudyLog.study_date >= first_day)
    if last_day:
        filters.append(StudyLog.study_date <= last_day)
    return filters

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
    
    filters = _build_filters(user_id, first_day, last_day)

    logs = (
        db.session.query(selected_date, Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(StudyLog.hour).label('total_hour'))
        .join(Field, StudyLog.field_id == Field.field_id)
        .filter(*filters)
        .group_by(selected_date, Field.fieldname, Field.color_code)
        .all()
    )

    return logs


# 横軸表示形式「分野別」の集計
def agg_by_fields(user_id: str, *, first_day: date | None = None, last_day: date | None = None):
    filters = _build_filters(user_id, first_day, last_day)

    logs = (
    db.session.query(Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(StudyLog.hour).label('total_hour'))
    .join(Field, StudyLog.field_id == Field.field_id)
    .filter(*filters)
    .group_by(Field.fieldname, Field.color_code)
    .order_by(func.sum(StudyLog.hour).desc())
    .all()
    )

    return logs