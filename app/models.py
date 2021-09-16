from app import db
from PIL import Image
import datetime
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin
from app import login   #login = LoginManager(app)


class User(UserMixin,db.Model):
    __table_args__ = {'extend_existing': True}  # to allow redefining table.

    id = db.Column(db.Integer,primary_key=True) #If not given, it will automatically be stored
    username = db.Column(db.String(64), index=True,unique=True)
    email = db.Column(db.String(120), index=True,unique=True)
    password_hash = db.Column(db.String(128))


    posts = db.relationship("Post",backref="author",lazy="dynamic")
    #This is not an actual database field, but a high-level view between users and posts
        #1 first argument to db.relationship is the model class that represents the "many" side of the relationship.
        #2 The backref argument defines the name of a field that will be added to the objects
            #of the "many" class that points back at the "one" object.
            #This will add a "post.author" expression that will return the user given a post.

    def __repr__(self):
        return '<User {}>'.format(self.username)

    #hashing
    def set_password(self,password):
        self.password_hash= generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password) # Boolean

#Fields are created as attribute of the db.Column class,
#which takes the field type as an argument

#optional fields such as index and unique is important in search efficiency


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))

    #to sort it in chronological order
    timestamp = db.Column(db.DateTime, \
                          index=True,\
                          default=datetime.datetime.utcnow)
        #These timestamps will be converted to the user's local time when they are displayed.


    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #The user_id field was initialized as a foreign key to user.id,
    # which means that it references an id value from the users table.


    def __repr__(self):
        return "<Post {}>".format(self.body)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

