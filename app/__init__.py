from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Инициализация Flask приложения
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Инициализация системы логина
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
