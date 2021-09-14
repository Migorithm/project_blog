from app import app
from flask import render_template,flash,redirect,url_for
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    title = {"title":"Welcome to My Blog!"}
    posts = [{
        "skill":"MongoDB",
            },
        {
            "skill": "Oracle",
        },
        {
            "skill": "Docker",
        },
        {
            "skill": "Spark",
        },
        {
            "skill": "Python",
        },
        {
            "skill": "Rest API",
        },
    ]
    return render_template("index.html",title=title,posts=posts)



@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm() #form object
    if form.validate_on_submit(): #on submission, it will validate the data.
# When the browser sends the GET request to receive the web page with the form, this if statements returns False,
# so the function skips the if statement and goes directly to render the template in the last line of the function.

        flash("Login User: {} :: Remember_me: {}".format(form.username.data,form.remember_me.data))
# When you call the flash() function, Flask stores the message,
        return redirect(url_for("index"))
    return render_template("login.html",title="Sign in",form=form)


@app.route("/ind")
def ind():
    return render_template("ind.html")