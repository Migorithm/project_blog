from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from PIL import Image



app = Flask(__name__)
#this config method will take all the attribute from Config object
app.config.from_object(Config)

db = SQLAlchemy(app)       #db object
migrate = Migrate(app,db)  #migration engine



from app import routes,models

#model module will define the structure of the db



#Image.open("../users_model.png").show()
#Explanation on fileds
# - id :: primary key
# - password_hash  :: to adopt security best practices, I will not be storing user passwords in the database.
                #  :: Instead of writing the passwords directly, gonna write password hashes which improve security.