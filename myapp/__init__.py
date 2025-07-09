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

@app.route('/')
def hello_world():
    return '<p>Hello World!</p>'

if __name__ == '__main__':
    print('Starting Flask application...')
    app.run(host='0.0.0.0', debug=True)