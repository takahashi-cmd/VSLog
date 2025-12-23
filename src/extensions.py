from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# インスタンスの作成
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
