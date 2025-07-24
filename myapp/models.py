from .app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DECIMAL, TIMESTAMP, extract, desc
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from matplotlib import font_manager
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from collections import defaultdict
import io
import base64
import platform

# matplotlibのフォント定義
font_path = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# SVGグラフのフォントにテキストを埋め込み
plt.rcParams['svg.fonttype'] = 'none'

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

class StudyLog(db.Model):
    __tablename__ = 'study_logs'

    study_log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    field_id = Column(Integer, ForeignKey('fields.field_id'), nullable=False)
    study_date = Column(Date, nullable=False)
    hour = Column(DECIMAL(6,1), nullable=False)
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

    # ユーザー毎の全学習履歴取得
    @classmethod
    def get_study_logs_all(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    # 学習総日数取得
    @classmethod
    def get_total_day(cls, user_id):
        total_day = db.session.query(func.count(func.distinct(cls.study_date))).filter_by(user_id=user_id).scalar()
        return int(total_day or 0)
    
    # 学習総時間取得
    @classmethod
    def get_total_hour(cls, user_id):
        total_hour = db.session.query(func.sum(cls.hour)).filter_by(user_id=user_id).scalar()
        return float(total_hour or 0.0)
    
    # 今週の学習時間（合計、平均）、学習日数の取得
    @classmethod
    def get_this_week_stats(cls, user_id):
        today = date.today()
        # 今週の月曜日を計算（週の開始）
        start_of_week = today - timedelta(days=today.weekday())
        # 今週の日曜日を計算（週の終わり）
        end_of_week = start_of_week + timedelta(days=6)

        # 今週の学習時間の合計
        total_hours = (
            db.session.query(func.sum(cls.hour))
            .filter(
                cls.user_id == user_id,
                cls.study_date >= start_of_week,
                cls.study_date <= end_of_week
            )
            .scalar()

        )
        total_hours = float(total_hours or 0.0)

        # 今週の学習日数
        study_days = (
            db.session.query(func.count(func.distinct(cls.study_date)))
            .filter(
                cls.user_id == user_id,
                cls.study_date >= start_of_week,
                cls.study_date <= end_of_week
            )
            .scalar()
        )

        # 今週の学習時間の平均（時間/週）
        average_per_day = total_hours / study_days if study_days else 0.0

        return {
            'start_date': start_of_week,
            'end_date': end_of_week,
            'total_hours': float(total_hours or 0.0),
            'study_days': study_days,
            'average_per_day': round(average_per_day, 2)
        }
    
    # 今週の学習時間のグラフ作成
    @classmethod
    def get_this_week_graph(cls, user_id):
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # 今週の学習ログを取得
        logs = (
            db.session.query(cls.study_date, Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(cls.hour))
            .join(Field, cls.field_id == Field.field_id)
            .filter(
                cls.user_id == user_id,
                cls.study_date >= start_of_week,
                cls.study_date <= end_of_week
            )
            .group_by(cls.study_date, Field.fieldname, Field.color_code)
            .all()
        )

        if not logs:
            return None

        # 日付リスト（月～日）
        week_days = [start_of_week + timedelta(days=i) for i in range(7)]
        date_format = '%#m/%#d(%a)' if platform.system() == 'Windows' else '%-m/%-d(%a)'
        data_labels = [d.strftime(date_format) for d in week_days]

        # 分野名のセット
        fieldnames = sorted(set(log[1] for log in logs))

        # 積み上げ用のデータ準備
        data = {field: [0] * 7 for field in fieldnames}
        color_map = {}
        for study_date, fieldname, color_code, hour in logs:
            color_map[fieldname] = color_code
            index = (study_date - start_of_week).days
            data[fieldname][index] = float(hour)
        
        # グラフ描画
        fig, ax = plt.subplots(figsize=(10, 4))
        bottom = [0] * 7
        for fieldname in sorted(data.keys()):
            ax.bar(data_labels, data[fieldname], bottom=bottom, label=fieldname, color=color_map.get(fieldname))
            bottom = [b + h for b, h in zip(bottom, data[fieldname])]
        
        ax.set_title(f'{start_of_week.strftime(date_format)}～の学習履歴')
        ax.grid(True)
        ax.set_ylabel('学習時間（時間）')
        column_totals = [sum(day) for day in zip(*data.values())]
        ymax = max(column_totals) + 1 if column_totals else 1
        ax.set_ylim(0, ymax)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        # 画像をsvg形式で生成する
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='svg')
        svg_data = buf.getvalue()
        plt.close(fig)

        return svg_data

    # 月間学習日数、学習時間（合計）、学習時間（平均）の取得
    @classmethod
    def get_month_stats(cls, user_id, month_str):
        year, month = map(int, month_str.split('-'))
        first_day = date(year, month, 1)
        month_num = calendar.monthrange(year, month)[1]
        last_day = date(year, month, month_num)

        total_hours = (
            db.session.query(func.sum(cls.hour))
            .filter(
                cls.user_id == user_id,
                cls.study_date >= first_day,
                cls.study_date <= last_day
            )
            .scalar()
        )

        study_days = (
            db.session.query(func.count(func.distinct(cls.study_date)))
            .filter(
                cls.user_id == user_id,
                cls.study_date >= first_day,
                cls.study_date <= last_day
            )
            .scalar()
        )

        average_per_day = total_hours / study_days if study_days else 0.0

        return {
            'total_hours': float(total_hours or 0.0),
            'study_days': study_days,
            'average_per_day': round(average_per_day, 1)
        }

    # 月間グラフ作成
    @classmethod
    def get_month_graph(cls, user_id, month_str):
        year, month = map(int, month_str.split('-'))
        first_day = date(year, month, 1)
        month_num = calendar.monthrange(year, month)[1]
        last_day = date(year, month, month_num)

        logs = (
            db.session.query(cls.study_date, Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(cls.hour))
        .join(Field, cls.field_id == Field.field_id)
        .filter(
            cls.user_id == user_id,
            cls.study_date >= first_day,
            cls.study_date <= last_day
        )
        .group_by(cls.study_date, Field.fieldname, Field.color_code)
        .all()
        )

        if not logs:
            return None

        month_days = [first_day + timedelta(days=i) for i in range(month_num)]
        date_format = '%#m/%#d(%a)' if platform.system() == 'Windows' else '%-m/%-d(%a)'
        data_labels = [d.strftime(date_format) for d in month_days]

        fieldnames = sorted(set(log[1] for log in logs))

        data = {field: [0] * month_num for field in fieldnames}
        color_map = {}
        for study_date, fieldname, color_code, hour in logs:
            color_map[fieldname] = color_code
            index = (study_date - first_day).days
            data[fieldname][index] = float(hour)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        bottom = [0] * month_num
        for fieldname in sorted(data.keys()):
            ax.bar(data_labels, data[fieldname], bottom=bottom, label=fieldname, color=color_map.get(fieldname))
            bottom = [b + h for b, h in zip(bottom, data[fieldname])]
        
        ax.set_title(f'{year}/{month}の学習履歴')
        ax.grid(True)
        ax.set_ylabel('学習時間（時間）')
        column_totals = [sum(day) for day in zip(*data.values())]
        ymax = max(column_totals) + 1 if column_totals else 1
        ax.set_ylim(0, ymax)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='svg')
        svg_data = buf.getvalue()
        plt.close(fig)

        return svg_data

    # 年間学習日数、学習時間（合計）、学習時間（平均）の取得
    @classmethod
    def get_year_stats(cls, user_id, year_str):
        year = int(year_str)
        first_day = date(year, 1, 1)
        last_day= date(year, 12, 31)

        total_hours = (
            db.session.query(func.sum(cls.hour))
            .filter(
                cls.user_id == user_id,
                cls.study_date >= first_day,
                cls.study_date <= last_day
            )
            .scalar()
        )

        study_days = (
            db.session.query(func.count(func.distinct(cls.study_date)))
            .filter(
                cls.user_id == user_id,
                cls.study_date >= first_day,
                cls.study_date <= last_day
            )
            .scalar()
        )

        average_per_day = total_hours / study_days if study_days else 0.0

        return {
            'total_hours': float(total_hours or 0.0),
            'study_days': study_days,
            'average_per_day': round(average_per_day, 1)
        }

    # 年間グラフの作成
    @classmethod
    def get_year_graph(cls, user_id, year_str):
        year = int(year_str)
        first_day = date(year, 1, 1)
        last_day= date(year, 12, 31)

        logs = (
            db.session.query(cls.study_date, Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(cls.hour))
            .join(Field, cls.field_id == Field.field_id)
            .filter(
                cls.user_id == user_id,
                cls.study_date >= first_day,
                cls.study_date <= last_day
            )
            .group_by(extract('month', cls.study_date), Field.fieldname, Field.color_code)
            .all()
        )

        if not logs:
            return None
        
        date_format = '%#Y/%#m' if platform.system() == 'Windows' else '%Y/%-m'
        data_labels = [
            date(year, int(month), 1).strftime(date_format)
            for month in range(1, 13)
        ]
        
        fieldnames = sorted(set(log[1] for log in logs))

        data = {field: [0] * 12 for field in fieldnames}
        color_map = {}
        for month, fieldname, color_code, hour in logs:
            color_map[fieldname] = color_code
            index = int(month) - 1
            data[fieldname][index] = float(hour)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        bottom = [0] * 12
        for fieldname in sorted(data.keys()):
            ax.bar(data_labels, data[fieldname], bottom=bottom, label=fieldname, color=color_map.get(fieldname))
            bottom = [b + h for b, h in zip(bottom, data[fieldname])]
        
        ax.set_title(f'{year}年の学習履歴')
        ax.grid(True)
        ax.set_ylabel('学習時間（時間）')
        column_totals = [sum(day) for day in zip(*data.values())]
        ymax = max(column_totals) + 1 if column_totals else 1
        ax.set_ylim(0, ymax)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='svg')
        svg_data = buf.getvalue()
        plt.close(fig)

        return svg_data

    # 分野別全期間グラフの作成
    @classmethod
    def get_all_time_graph_by_field(cls, user_id):
        logs = (
            db.session.query(Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(cls.hour))
            .join(Field, cls.field_id == Field.field_id)
            .filter(cls.user_id == user_id)
            .group_by(Field.fieldname, Field.color_code)
            .order_by(func.sum(cls.hour).desc())
            .all()
        )

        if not logs:
            return None

        data = {fieldname: float(hour) for fieldname, _, hour in logs}
        color_map = {fieldname: color_code for fieldname, color_code, _ in logs}

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(data.keys(), data.values(), color=[color_map[f] for f in data.keys()])
        
        ax.set_title('分野別全期間の学習履歴')
        ax.grid(True)
        ax.set_ylabel('学習時間（時間）')
        max_hour = max(data.values()) if data else 0
        ax.set_ylim(0, max_hour + 1)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='svg')
        svg_data = buf.getvalue()
        plt.close(fig)

        return svg_data

    # 分野別年間グラフ作成
    @classmethod
    def get_year_graph_by_field(cls, user_id, year_str):
        year = int(year_str)
        first_day = date(year, 1, 1)
        last_day = date(year, 12, 31)

        logs = (
            db.session.query(Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(cls.hour))
            .join(Field, cls.field_id == Field.field_id)
            .filter(cls.user_id == user_id,
                    cls.study_date >= first_day,
                    cls.study_date <= last_day
            )
            .group_by(Field.fieldname, Field.color_code)
            .order_by(func.sum(cls.hour).desc())
            .all()
        )

        data = {fieldname: float(hour) for fieldname, _, hour in logs}
        color_map = {fieldname: color_code for fieldname, color_code, _ in logs}

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(data.keys(), data.values(), color=[color_map[f] for f in data.keys()])
        
        ax.set_title(f'{year}年の分野別学習履歴')
        ax.grid(True)
        ax.set_ylabel('学習時間（時間）')
        max_hour = max(data.values()) if data else 0
        ax.set_ylim(0, max_hour + 1)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='svg')
        svg_data = buf.getvalue()
        plt.close(fig)

        return svg_data

    # 分野別月間グラフ作成
    @classmethod
    def get_month_graph_by_field(cls, user_id, month_str):
        year, month = map(int, month_str.split('-'))
        first_day = date(year, month, 1)
        month_num = calendar.monthrange(year, month)[1]
        last_day = date(year, month, month_num)

        logs = (
            db.session.query(Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(cls.hour))
            .join(Field, cls.field_id == Field.field_id)
            .filter(cls.user_id == user_id,
                    cls.study_date >= first_day,
                    cls.study_date <= last_day
            )
            .group_by(Field.fieldname, Field.color_code)
            .order_by(func.sum(cls.hour).desc())
            .all()
        )

        data = {fieldname: float(hour) for fieldname, _, hour in logs}
        color_map = {fieldname: color_code for fieldname, color_code, _ in logs}

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(data.keys(), data.values(), color=[color_map[f] for f in data.keys()])
        
        ax.set_title(f'{year}年{month}月の分野別学習履歴')
        ax.grid(True)
        ax.set_ylabel('学習時間（時間）')
        max_hour = max(data.values()) if data else 0
        ax.set_ylim(0, max_hour + 1)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='svg')
        svg_data = buf.getvalue()
        plt.close(fig)

        return svg_data