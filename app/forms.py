from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")



#when calling, you can call it by just LoginForm()
#If you want to get an access to each attribute, simply dot it.
# For example, ::
# form.username.label
# form.username.data
# form.username.errors