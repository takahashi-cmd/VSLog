# StudyLogの読み込み用のクエリ
from __future__ import annotations

from datetime import date, datetime

from ....extensions import db
from ....models import Field
from ....models import StudyLog

# ユーザー毎の全学習履歴取得
def read_all(user_id: str):
    return StudyLog.query.filter_by(user_id=user_id).all()

# 学習日に応じたユーザー毎の学習履歴取得
def read_by_date(user_id: str, date_str: str):
    study_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    logs = (
        db.session.query(StudyLog.study_log_id, StudyLog.study_date, Field.fieldname.label('fieldname'), StudyLog.content, StudyLog.hour)
        .join(Field, StudyLog.field_id == Field.field_id)
        .filter(
        StudyLog.user_id == user_id,
        StudyLog.study_date == study_date
        )
        .all()
    )
    return logs

# 月に応じたユーザー毎の学習履歴取得
def read_by_month(user_id: str, first_day: date, last_day: date):
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
