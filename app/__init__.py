from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from PIL import Image
from flask_login import LoginManager  #session handler



app = Flask(__name__)
#this config method will take all the attribute from Config object
app.config.from_object(Config)

db = SQLAlchemy(app)       #db object
migrate = Migrate(app,db)  #migration engine

login = LoginManager(app)
login.login_view ='login'  #to make login necessary

from app import routes,models

#model module will define the structure of the db


