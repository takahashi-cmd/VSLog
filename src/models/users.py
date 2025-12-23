from flask_login import UserMixin
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions
from flask_bcrypt import generate_password_hash, check_password_hash

from ..extensions import db

# テーブル・カラム作成
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=functions.current_timestamp())

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