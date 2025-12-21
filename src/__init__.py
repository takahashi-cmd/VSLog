# アプリファクトリ
from dotenv import load_dotenv
from flask import Flask

from .config import Config
from .extensions import db, migrate, login_manager

def create_app(config_object=Config) -> Flask:
    # .envファイルの読み込み（カレントディレクトリがルートである前提）
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object(config_object)

    # extensionsを初期化
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 未認証のユーザーがリダイレクトされるビュー関数とメッセージを設定
    login_manager.login_view = 'login_view'
    login_manager.login_message = 'ログインが必要です。先にログインしてください。'

    @login_manager.user_loader
    def load_user(user_id):
        from .models.users import User
        return User.query.get(user_id)
    
    # from .blueprints import 

    return app