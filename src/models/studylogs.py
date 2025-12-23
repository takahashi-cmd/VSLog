from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DECIMAL
from sqlalchemy.orm import relationship

from ..extensions import db

class StudyLog(db.Model):
    __tablename__ = 'study_logs'

    study_log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    field_id = Column(Integer, ForeignKey('fields.field_id'), nullable=False)
    study_date = Column(Date, nullable=False)
    hour = Column(DECIMAL(6,2), nullable=False)
    content = Column(Text, nullable=False)

    # users,fieldsに紐づけし、双方向でアクセス
    users = relationship('User', back_populates='study_logs')
    fields = relationship('Field', back_populates='study_logs')

    def __init__(self, user_id, field_id, study_date, hour, content):
        self.user_id = user_id
        self.field_id = field_id
        self.study_date =study_date
        self.hour = hour
        self.content = content