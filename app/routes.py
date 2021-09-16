from app import app
from flask import render_template,flash,redirect,url_for,request
from app.forms import LoginForm , RegistrationForm
from flask_login import current_user,login_user , logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db


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
        if user is None or not user.check_password(form.password.data):
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
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template("register.html",title="Register",form=form)