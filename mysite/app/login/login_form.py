from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()],
                       render_kw={'placeholder': 'Please enter your username'})
    password = PasswordField("Password", validators=[DataRequired()],
                             render_kw={'placeholder': 'Please enter your password'})
    remember_me = BooleanField("Remember me.")
    submit = SubmitField("Login")
