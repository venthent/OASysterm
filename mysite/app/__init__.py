from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from ..config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager=LoginManager()
moment=Moment()
login_manager.login_view='auth.login'


def creat_app(config_name):
    from .auth import auth as login_bp
    from .main import main as main_bp

    app=Flask(__name__)
    app.config.from_object(config.get(config_name))
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    app.register_blueprint(login_bp)
    app.register_blueprint(main_bp,url_prefix='/main')
    return app
