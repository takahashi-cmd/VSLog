from .app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# テーブル・カラム作成
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, server_default=func.now())

    # fields,study_logsに紐づけし、双方向でアクセス
    fields = relationship('Field', back_populates='users')
    study_logs = relationship('StudyLog', back_populates='users')

    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    # get_idをオーバーライドして、login_user()を使用できるようにする
    def get_id(self):
        return self.user_id

    def validate_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

class Field(db.Model):
    __tablename__ = 'fields'

    field_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    fieldname = Column(String(20, collation='utf8mb4_general_ci'), nullable=False)
    color_code = Column(String(7), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, server_default=func.now())

    # users,study_logsに紐づけし、双方向でアクセス
    users = relationship('User', back_populates='fields')
    study_logs = relationship('StudyLog', back_populates='fields')

    def __init__(self, user_id, fieldname, color_code):
        self.user_id = user_id
        self.fieldname = fieldname
        self.color_code = color_code
    
    @classmethod
    def get_fields_all(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

class StudyLog(db.Model):
    __tablename__ = 'study_logs'

    study_log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    field_id = Column(Integer, ForeignKey('fields.field_id'), nullable=False)
    study_date = Column(Date, nullable=False)
    hours = Column(DECIMAL(6,1), nullable=False)
    content = Column(Text, nullable=False)

    # users,fieldsに紐づけし、双方向でアクセス
    users = relationship('User', back_populates='study_logs')
    fields = relationship('Field', back_populates='study_logs')
