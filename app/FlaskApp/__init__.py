from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_mail import Mail
from flask_wtf import CSRFProtect
from FlaskApp.config import Config

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    from FlaskApp.main.routes import main
    from FlaskApp.admin.routes import admin
    from FlaskApp.apis.resources import apis
    from FlaskApp.poll.routes import poll

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(apis)
    app.register_blueprint(poll)

    return app