import os

class Config:
    SECRET_KEY = os.environ.get('POLLAPP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('POLLAPP_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('POLLAPP_MAIL_USER')
    MAIL_PASSWORD = os.environ.get('POLLAPP_MAIL_PWD')
    MAIL_SUPPRESS_SEND = False
