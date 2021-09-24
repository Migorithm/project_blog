import os
#to get absolute path
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    #db uri protocol ::
    #       Flask-SQLAlchemy extension takes the location of DB from the SQLALCHEMY_DATABASE_URI configuration variable.
    #       You can do the same thing through, for example,
    #       app.config["SQLALCHEMY_DATABASE_URI"] = "oracle+cx_oracle://migo:admin1234@127.0.0.1:1521/?service_name=XE"
    SQLALCHEMY_DATABASE_URI= os.environ.get("DATABASE_URL") or\
        'sqlite:///' +os.path.join(basedir,"app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS= False
    #if true, this sends a signal to application every time a change is about to be made in DB

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['saka90030@naver.com']



