from app import app
from flask import render_template,flash,redirect,url_for,request
from app.forms import LoginForm , RegistrationForm,EditProfileForm
from flask_login import current_user,login_user , logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db
from datetime import datetime
from pytz import timezone,utc

@app.route("/")
@app.route("/index")
@login_required  #If the user navigates to /index, @login_required decorator will intercept the request
def index():     # /login?next=/index. if user is not logged in.
    title = {"title":"Welcome to My Blog!"}
    posts = [
        {
            'author': {'username': 'Migo'},
            'body': 'Beautiful day in Bucheon!'
        },
        {
            'author': {'username': 'Alex'},
            'body': "I'm so happy!"
        }
    ]
    return render_template("index.html",title=title,posts=posts)



@app.route("/login",methods=["GET","POST"])
def login():
    #1
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    #2
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data): #password check
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user,remember=form.remember_me.data) #true or false. This creates a session for the user.
        #3
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page=url_for('index')
        return redirect(next_page)
    return render_template("login.html",title="Sign in",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm() #can decide which form has been used and you would use
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data) #create User instance first
        user.set_password(form.password.data)                          #and set the password to hash the given, raw password
        db.session.add(user)                                              #How can you ensure that the password was given? -> at form level.
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template("register.html",title="Register",form=form)



@app.route('/user/<username>')  #{{ url_for('user', username=current_user.username) }}
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

def Korean_time():
    KST = timezone("Asia/Seoul")
    current_time = utc.localize(datetime.utcnow()).astimezone(KST) #you may want to change this
    return current_time

@app.before_request
def before_request():
    if current_user.is_authenticated:
        #Koreanized

        current_user.last_seen = Korean_time()
        db.session.commit()
        #No db.session.add(user)?
        #-> it's called already when current_user was referenced

@app.route("/edit_profile",methods=["GET","POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data #change name
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method =="GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html",title="Edit Profile",form=form)