from .app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime

# テーブル・カラム作成
class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, server_default=func.now())

    # study_logsに紐づけし、双方向でアクセス
    study_logs = relationship('StudyLog', back_populates='users')

    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

class Field(db.Model):
    __tablename__ = 'fields'

    field_id = Column(Integer, primary_key=True)
    fieldname = Column(String(20), nullable=False)
    color_code = Column(String(7), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, server_default=func.now())

    # study_logsに紐づけし、双方向でアクセス
    study_logs = relationship('StudyLog', back_populates='fields')

class StudyLog(db.Model):
    __tablename__ = 'study_logs'

    study_log_id = Column(Integer, primary_key=True)
    study_date = Column(Date, nullable=False)
    hours = Column(DECIMAL(6,1), nullable=False)
    field_id = Column(Integer, ForeignKey('fields.field_id'), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)

    # users,fieldsに紐づけし、双方向でアクセス
    users = relationship('User', back_populates='study_logs')
    fields = relationship('Field', back_populates='study_logs')
