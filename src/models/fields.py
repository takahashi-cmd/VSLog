from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions

from ..extensions import db

class Field(db.Model):
    __tablename__ = 'fields'

    field_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    fieldname = Column(String(20, collation='utf8mb4_general_ci'), nullable=False)
    color_code = Column(String(7), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=functions.current_timestamp())

    # users,study_logsに紐づけし、双方向でアクセス
    # study_logsとはcascade設定をし、fieldが削除されれば、関連するstudy_logsも削除するよう設定
    users = relationship('User', back_populates='fields')
    study_logs = relationship('StudyLog', back_populates='fields', cascade='all, delete-orphan')

    def __init__(self, user_id, fieldname, color_code):
        self.user_id = user_id
        self.fieldname = fieldname
        self.color_code = color_code
    
    @classmethod
    def get_fields_all(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_field_id(cls, user_id, fieldname):
        field = cls.query.filter_by(user_id=user_id, fieldname=fieldname).first()
        return field.field_id if field else None