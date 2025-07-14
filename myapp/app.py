import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# .envファイルの読み込み（カレントディレクトリがルートである前提）
load_dotenv()

# Flaskインスタンス生成
app = Flask(__name__)

# appのconfig設定
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}'
    f'@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# dbにappをバインド
db = SQLAlchemy(app)

# migrateにapp,dbをバインド
migrate = Migrate(app, db)

# LoginManagerのインスタンス化
login_manager = LoginManager()

# LoginManagerとFlaskの紐づけ
login_manager.init_app(app)

# 未認証のユーザーがリダイレクトされるビュー関数とメッセージを設定
login_manager.login_view = 'login_view'
login_manager.login_message = 'ログインが必要です。先にログインしてください。'

# ユーザー情報を読み込む関数load_userをFlask_loginに登録
@login_manager.user_loader
def load_user(user_id):
    # 循環参照を避けるため、関数内で遅延インポートする
    from .models import User
    return User.query.get(str(user_id))

# FlaskアプリとDBオブジェクトが完全に初期化されたあとにmodelsを読み込む(循環参照を回避)
# viewsのインポート
from . import models, views

