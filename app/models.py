from app import db
from PIL import Image
import datetime
from pytz import timezone, utc

KST = timezone("Asia/Seoul")


class User(db.Model):
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
        #so, don't have to put something like --
        #   lambda :utc.localize(datetime.datetime.utcnow()).astimezone(KST)


    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #The user_id field was initialized as a foreign key to user.id,
    # which means that it references an id value from the users table.


    def __repr__(self):
        return "<Post {}>".format(self.body)





""" 
the model created now define the initial schema for this application 
But as the application continues to grow, 
it's likely that you need to make changes to that structure -- removing, modifying..

Alembic makes these schema changes in a way that it doesn't require the DB to be recreated.

To accomplish this task:: 
    1. Alembic maintains a migration repository where it stores migration scripts 
    2. Each time a change is made, migration is added to the repository with details.
    3. You have to use flask-native command "flask db init", exposed by Flask-Migrate
    
    #first migration
    4. With the migration repository in place,it is time to create 
        the first database migration, which will include the "users table" that 
        maps to the "User database model".
    
    5. "flask db migrate" sub-command generates theise automatic migration 
    
    6.  upgrade()   :: apply the migration, 
        downgrade() :: remove them.
    
    7. The flask db migrate command does not make any changes to the database, 
       to apply the chanages, "flask db upgrade" command must be used.
            ::Because this application uses SQLite, 
              the upgrade command will detect that a database does not exist 
              and will create it. (app.db)
              
    8. When working with database server such as Oracle or Mysql, 
       you have to create the DB in the DB server before running upgrade. 
    
    
"""


