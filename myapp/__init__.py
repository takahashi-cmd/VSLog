import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

# FlaskアプリとDBオブジェクトが完全に初期化されたあとにモデルを読み込む(循環参照を回避)
# viewsのインポート
from myapp import models, views