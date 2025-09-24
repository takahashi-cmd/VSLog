from .app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DECIMAL, DATETIME, extract, desc
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from matplotlib import font_manager
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from collections import defaultdict
import io, re
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

    # ユーザー毎の全学習履歴取得
    @classmethod
    def get_study_logs_all(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    # 学習日に応じたユーザー毎の学習履歴取得
    @classmethod
    def get_study_logs_by_study_date(cls, user_id, date_str):
        study_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        logs = (
            db.session.query(cls.study_log_id, cls.study_date, Field.fieldname.label('fieldname'), cls.content, cls.hour)
            .join(Field, cls.field_id == Field.field_id)
            .filter(
            cls.user_id == user_id,
            cls.study_date == date_str
            )
            .all()
        )

        if not logs:
            return None
        
        return logs

    # 月に応じたユーザー毎の学習履歴取得
    @classmethod
    def get_study_logs_by_study_month(cls, user_id, month_year_str, month_str):
        year = int(month_year_str)
        month = int(month_str)
        first_day = date(year, month, 1)
        month_num = calendar.monthrange(year, month)[1]
        last_day = date(year, month, month_num)

        logs = (
            db.session.query(cls.study_log_id, cls.study_date, Field.fieldname.label('fieldname'), cls.content, cls.hour)
            .join(Field, cls.field_id == Field.field_id)
            .filter(
            cls.user_id == user_id,
            cls.study_date >= first_day,
            cls.study_date <= last_day
            )
            .all()
        )
        return logs

    # 統計値取得の共通関数
    @classmethod
    def common_stats_process(cls, user_id, first_day, last_day):
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

        average_per_day = total_hours / study_days if study_days else 0.00

        return {
            'total_hours': f'{total_hours:.2f}' or 0.00,
            'study_days': study_days,
            'average_per_day': f'{average_per_day:.2f}'
        }

    # 年月日別グラフ取得の共通関数
    @classmethod
    def common_graph_by_days(cls, user_id, period, verticalAxis, graphType, first_day=None, last_day=None, year=None, month=None, month_num=None):
        if period == 'this_week' or period == 'last_week' or period == 'month':
            selected_date = cls.study_date
        elif period == 'year':
            selected_date = func.date_format(cls.study_date, '%m').label('month')
        elif period == 'all':
            selected_date = func.date_format(cls.study_date, '%Y').label('year')
        
        filters = [cls.user_id == user_id]
        if first_day:
            filters.append(cls.study_date >= first_day)
        if last_day:
            filters.append(cls.study_date <= last_day)

        logs = (
            db.session.query(selected_date, Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(cls.hour).label('total_hour'))
            .join(Field, cls.field_id == Field.field_id)
            .filter(*filters)
            .group_by(selected_date, Field.fieldname, Field.color_code)
            .all()
        )

        if not logs:
            return None

        # 日付（X軸）のラベル、ラベルフォーマットの設定
        if period == 'this_week' or period == 'last_week':
            date_num = 7 # 1週間の日数
            date_format = '%#m/%#d(%a)' if platform.system() == 'Windows' else '%-m/%-d(%a)'
            set_days = [first_day + timedelta(days=i) for i in range(date_num)]
            data_labels = [d.strftime(date_format) for d in set_days]

        elif period == 'month' and year and month and month_num:
            date_num = month_num # 月毎の日数
            date_format = '%#m/%#d(%a)' if platform.system() == 'Windows' else '%-m/%-d(%a)'
            set_days = [first_day + timedelta(days=i) for i in range(date_num)]
            data_labels = [d.strftime(date_format) for d in set_days]

        elif period == 'year':
            date_num = 12 # 12ヶ月
            date_format = '%#Y/%#m' if platform.system() == 'Windows' else '%Y/%-m'
            data_labels = [
            date(year, int(month), 1).strftime(date_format)
            for month in range(1, date_num + 1)
            ]

        elif period == 'all':
            date_list = list(sorted(set(log[0] for log in logs)))
            date_num = len(date_list) # logsに登録されているyearの数を取得
            date_format = '%#Y' if platform.system() == 'Windows' else '%Y'
            data_labels = date_list

        # 分野名のセット
        fieldnames = sorted(set(log[1] for log in logs))

        # 積み上げ用のデータ準備
        data = {field: [0] * date_num for field in fieldnames}
        color_map = {}
        for selected_date, fieldname, color_code, hour in logs:
            color_map[fieldname] = color_code
            if period == 'this_week' or period == 'last_week' or period == 'month':
                index = (selected_date - first_day).days
            elif period == 'year':
                index = int(selected_date) - 1
            elif period == 'all':
                index = date_list.index(selected_date)

            # 縦軸の表示形式が「時間（time）」と「％（percent）」で条件分岐
            if verticalAxis == 'time':
                data[fieldname][index] = float(hour)
            elif verticalAxis == 'percent':
                total_hour = 0
                percentage = 100
                for _, _, _, hour_p in logs:
                    total_hour += float(hour_p)
                data[fieldname][index] = round((float(hour) / float(total_hour) * percentage), 2)
        
        # グラフ描画
        fig, ax = plt.subplots(figsize=(10, 4))
        bottom = [0] * date_num
        # グラフ種類によって条件分岐（棒グラフ、円グラフ、折れ線グラフ）
        # 棒グラフの設定
        if graphType == 'bar':
            for fieldname in sorted(data.keys()):
                ax.bar(data_labels, data[fieldname], bottom=bottom, label=fieldname, color=color_map.get(fieldname))
                bottom = [b + h for b, h in zip(bottom, data[fieldname])]
            ax.grid(True)
            ax.set_xlabel('年月日')
            if verticalAxis == 'time':
                ax.set_ylabel('学習時間（時間）')
            elif verticalAxis == 'percent':
                ax.set_ylabel('学習時間（%）')
            column_totals = [sum(day) for day in zip(*data.values())]
            ymax_val = max(column_totals) if column_totals else 0
            padding = max(1, ymax_val * 0.1)
            ymax = ymax_val + padding
            ax.set_ylim(0, ymax)
            if period == 'month':
                plt.setp(ax.get_xticklabels(), rotation=270, ha='center')
            ax.legend(loc='upper left', bbox_to_anchor=(1.04, 1), edgecolor='black', borderaxespad=0)
            for x, y in zip(data_labels, bottom):
                if y != 0:
                    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom')
        
        # 円グラフの設定
        elif graphType == 'pie':
            for fieldname in sorted(data.keys()):
                bottom = [b + h for b, h in zip(bottom, data[fieldname])]
            # bottomが0の時のbottomとdata_labelsを除外する関数
            def filter_zero(bottom, data_labels):
                filtered = [(b, l) for b, l in zip(bottom, data_labels) if b > 0]
                if not filtered:
                    return [], []
                b, l = zip(*filtered)
                return list(b), list(l)
            # 時間と％の場合で出力を変更する関数
            def format_time(pct, allvalues):
                total = sum(allvalues)
                value = pct/100 * total
                if verticalAxis == 'time':
                    return f'{value:.2f}時間'
                elif verticalAxis == 'percent':
                    return f'{value:.2f}%'
            b, l = filter_zero(bottom, data_labels)
            ax.pie(x=b, labels=l, counterclock=False, startangle=90, autopct=lambda pct: format_time(pct, b))
            ax.axis('equal')
            ax.legend(loc='upper left', bbox_to_anchor=(0.8, 1), edgecolor='black', borderaxespad=0)

        # 折れ線グラフの設定
        elif graphType == 'line':
            for fieldname in sorted(data.keys()):
                ax.plot(data_labels, data[fieldname], '-', color=color_map.get(fieldname), linewidth=1, alpha=1, marker='.', label=fieldname)
            ax.grid(True)
            ax.set_xlabel('年月日')
            if verticalAxis == 'time':
                ax.set_ylabel('学習時間（時間）')
            elif verticalAxis == 'percent':
                ax.set_ylabel('学習時間（%）')
            column_totals = [max(day) for day in zip(*data.values())]
            ymax_val = max(column_totals) if column_totals else 0
            padding = max(1, ymax_val * 0.1)
            ymax = ymax_val + padding
            ax.set_ylim(0, ymax)
            if period == 'month':
                plt.setp(ax.get_xticklabels(), rotation=270, ha='center')
            ax.legend(loc='upper left', bbox_to_anchor=(1.04, 1), edgecolor='black', borderaxespad=0)
            for fieldname in sorted(data.keys()):
                for x, y in zip(data_labels, data[fieldname]):
                    if y != 0:
                        plt.text(x, round(y, 2), round(y, 2), ha='center', va='bottom')
        
        print(f'bottom:{bottom}, data_labels:{data_labels}')
        
        # グラフタイトル【共通】
        if period == 'this_week' or period == 'last_week':
            ax.set_title(f'{first_day.strftime(date_format)}～{last_day.strftime(date_format)}の学習履歴', y=1.04)
        elif period == 'month' and year and month and month_num:
            ax.set_title(f'{year}年{month}月1日～{month}月{month_num}日の学習履歴', y=1.04)
        elif period == 'year':
            date_format_head = '%#Y年%#m月' if platform.system() == 'Windows' else '%Y年%-m月'
            ax.set_title(f'{first_day.strftime(date_format_head)}～{last_day.strftime(date_format_head)}までの学習履歴', y=1.04)
        elif period == 'all':
            ax.set_title(f'年月日別全期間の学習履歴', y=1.04)

        # 画像をsvg形式で生成する
        buf = io.BytesIO()
        fig.tight_layout()
        plt.savefig(buf, format='svg', bbox_inches='tight') # 画像ファイルとして保存
        plt.close(fig) # 図window(fig)を閉じてpyplotから登録を解除
        svg_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        return svg_b64

    # 分野別グラフ取得の共通関数
    @classmethod
    def common_graph_by_fields(cls, user_id, period, verticalAxis, graphType, first_day=None, last_day=None, year=None, month=None, month_num=None):
        filters = [cls.user_id == user_id]
        if first_day:
            filters.append(cls.study_date >= first_day)
        if last_day:
            filters.append(cls.study_date <= last_day)

        logs = (
        db.session.query(Field.fieldname.label('fieldname'), Field.color_code.label('color_code'), func.sum(cls.hour).label('total_hour'))
        .join(Field, cls.field_id == Field.field_id)
        .filter(*filters)
        .group_by(Field.fieldname, Field.color_code)
        .order_by(func.sum(cls.hour).desc())
        .all()
    )

        if not logs:
            return None

        date_format = '%#m/%#d(%a)' if platform.system() == 'Windows' else '%-m/%-d(%a)'
        if verticalAxis == 'time':
            data = {fieldname: float(hour) for fieldname, _, hour in logs}
        elif verticalAxis == 'percent':
            total_hour = 0
            percentage = 100
            for _, _, hour in logs:
                total_hour += float(hour)
            data = {fieldname: round((float(hour) / float(total_hour) * percentage), 1) for fieldname, _, hour in logs}
        color_map = {fieldname: color_code for fieldname, color_code, _ in logs}

        # グラフ描画
        fig, ax = plt.subplots(figsize=(10, 4))
        # グラフ種類によって条件分岐（棒グラフ、円グラフ、折れ線グラフ）
        # 棒グラフの設定
        if graphType == 'bar':
            ax.bar(data.keys(), data.values(), color=[color_map[f] for f in data.keys()])
            ax.grid(True)
            ax.set_xlabel('学習分野')
            if verticalAxis == 'time':
                ax.set_ylabel('学習時間（時間）')
            elif verticalAxis == 'percent':
                ax.set_ylabel('学習時間（%）')
            ymax_val = max(data.values()) if data else 0
            padding = max(1, ymax_val * 0.1)
            ymax = ymax_val + padding
            ax.set_ylim(0, ymax)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='center')
            for x, y in zip(data.keys(), data.values()):
                plt.text(x, y, f'{y:.2f}', ha='center', va='bottom')

        # 円グラフの設定
        elif graphType == 'pie':
            # 時間と％の場合で出力を変更する関数
            def format_time(pct, allvalues):
                total = sum(allvalues)
                value = pct/100 * total
                if verticalAxis == 'time':
                    return f'{value:.2f}時間'
                elif verticalAxis == 'percent':
                    return f'{value:.2f}%'
            ax.pie(x=list(data.values()), labels=list(data.keys()), colors=[color_map[f] for f in data.keys()], counterclock=False, startangle=90, autopct=lambda pct: format_time(pct, list(data.values())))
            ax.axis('equal')
            ax.legend(loc='upper left', bbox_to_anchor=(0.8, 1), edgecolor='black', borderaxespad=0)
        
        # 折れ線グラフの設定（学習分野では表示しないようガード処理）
        elif graphType == 'line':
            return None

        # グラフタイトル【共通】
        if period == 'this_week' or period == 'last_week':
            ax.set_title(f'{first_day.strftime(date_format)}～{last_day.strftime(date_format)}の学習履歴', y=1.04)
        elif period == 'month' and year and month and month_num:
            ax.set_title(f'{year}年{month}月1日～{month}月{month_num}日の分野別学習履歴', y=1.04)
        elif period == 'year' and year:
            ax.set_title(f'{year}年の分野別学習履歴', y=1.04)
        elif period == 'all':
            ax.set_title('分野別全期間の学習履歴', y=1.04)

        buf = io.BytesIO()
        fig.tight_layout()
        plt.savefig(buf, format='svg', bbox_inches='tight')
        plt.close(fig)
        svg_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        return svg_b64

    # 今週の学習時間（合計、平均）、学習日数の取得
    @classmethod
    def get_this_week_stats(cls, user_id):
        today = date.today()
        first_day = today - timedelta(days=today.weekday())
        last_day = first_day + timedelta(days=6)

        return StudyLog.common_stats_process(user_id, first_day, last_day)

    # 今週のグラフ作成
    @classmethod
    def get_this_week_graph(cls, user_id, period, horizontalAxis, verticalAxis, graphType):
        today = date.today()
        first_day = today - timedelta(days=today.weekday())
        last_day = first_day + timedelta(days=6)

        if horizontalAxis == 'days':
            return StudyLog.common_graph_by_days(user_id, period, verticalAxis, graphType, first_day, last_day)
        
        elif horizontalAxis == 'fields':
            return StudyLog.common_graph_by_fields(user_id, period, verticalAxis, graphType, first_day, last_day)

    # 先週の学習時間（合計、平均）、学習日数の取得
    @classmethod
    def get_last_week_stats(cls, user_id):
        today = date.today()
        first_day = today - timedelta(days=today.weekday() + 7)
        last_day = first_day + timedelta(days=6)

        return StudyLog.common_stats_process(user_id, first_day, last_day)

    # 先週のグラフ作成
    @classmethod
    def get_last_week_graph(cls, user_id, period, horizontalAxis, verticalAxis, graphType):
        today = date.today()
        first_day = today - timedelta(days=today.weekday() + 7)
        last_day = first_day + timedelta(days=6)

        if horizontalAxis == 'days':
            return StudyLog.common_graph_by_days(user_id, period, verticalAxis, graphType, first_day, last_day)

        elif horizontalAxis == 'fields':
            return StudyLog.common_graph_by_fields(user_id, period, verticalAxis, graphType, first_day, last_day)

    # 月間学習日数、学習時間（合計）、学習時間（平均）の取得
    @classmethod
    def get_month_stats(cls, user_id, month_year_str, month_str):
        year = int(month_year_str)
        month = int(month_str)
        first_day = date(year, month, 1)
        month_num = calendar.monthrange(year, month)[1]
        last_day = date(year, month, month_num)

        return StudyLog.common_stats_process(user_id, first_day, last_day)

    # 月間グラフ作成
    @classmethod
    def get_month_graph(cls, user_id, period, horizontalAxis, verticalAxis, graphType, month_year_str, month_str):
        year = int(month_year_str)
        month = int(month_str)
        first_day = date(year, month, 1)
        month_num = calendar.monthrange(year, month)[1]
        last_day = date(year, month, month_num)

        if horizontalAxis == 'days':
            return StudyLog.common_graph_by_days(user_id, period, verticalAxis, graphType, first_day, last_day, year, month, month_num)
        elif horizontalAxis == 'fields':
            return StudyLog.common_graph_by_fields(user_id, period, verticalAxis, graphType, first_day, last_day, year, month, month_num)

    # 年間学習日数、学習時間（合計）、学習時間（平均）の取得
    @classmethod
    def get_year_stats(cls, user_id, year_str):
        year = int(year_str)
        first_day = date(year, 1, 1)
        last_day= date(year, 12, 31)

        return StudyLog.common_stats_process(user_id, first_day, last_day)

    # 年間グラフ作成
    @classmethod
    def get_year_graph(cls, user_id, period, horizontalAxis, verticalAxis, graphType, year_str):
        year = int(year_str)
        first_day = date(year, 1, 1)
        last_day= date(year, 12, 31)

        if horizontalAxis == 'days':
            return StudyLog.common_graph_by_days(user_id, period, verticalAxis, graphType, first_day, last_day, year)
        elif horizontalAxis == 'fields':
            return StudyLog.common_graph_by_fields(user_id, period, verticalAxis, graphType, first_day, last_day, year)

    # 全期間の学習日数取得
    @classmethod
    def get_total_day(cls, user_id):
        total_day = db.session.query(func.count(func.distinct(cls.study_date))).filter_by(user_id=user_id).scalar()
        return int(total_day or 0)

    # 全期間の学習時間取得
    @classmethod
    def get_total_hour(cls, user_id):
        total_hour = db.session.query(func.sum(cls.hour)).filter_by(user_id=user_id).scalar()
        return float(total_hour or 0.0)

    # 全期間グラフ作成
    @classmethod
    def get_all_time_graph(cls, user_id, period, horizontalAxis, verticalAxis, graphType):
        if horizontalAxis == 'days':
            return StudyLog.common_graph_by_days(user_id, period, verticalAxis, graphType)
        elif horizontalAxis == 'fields':
            return StudyLog.common_graph_by_fields(user_id, period, verticalAxis, graphType)


