import os

class Config:
    SECREAT_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    MAIL_SERVER = 'smtp.googleemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')