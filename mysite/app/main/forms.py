from flask_wtf import FlaskForm
from wtforms import SubmitField,RadioField,StringField,PasswordField,SelectField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    name=StringField("Account name:",validators=[DataRequired()],render_kw={'placeholder': 'Username,for login'})
    real_name=StringField("Real name:",validators=[DataRequired()])
    position=SelectField(label="Job position:",choices=[('Staff','Staff'),('Manager','Manager'),('Boss','Boss')])
    submit=SubmitField('Add')
