from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, SelectField,TextAreaField
from wtforms.validators import DataRequired, Length
from ..models import User


class AccountForm(FlaskForm):
    name = StringField("Account name:", validators=[DataRequired(), Length(0, 20)],
                       render_kw={'placeholder': 'Username,for login'})
    real_name = StringField("Real name:", validators=[DataRequired()])
    position = SelectField(label="Job position:",
                           choices=[('Staff', 'Staff'), ('Manager', 'Manager'), ('Boss', 'Boss')])

    permission = SelectField(label="Permission:",
                             choices=[('Administrator', 'Administrator'), ('User', 'User')])

    old_password = PasswordField("Old password:", render_kw={
        'placeholder': 'If you write nothing,origional password will not be changed.'})

    new_password = PasswordField("New password:")
    confirm_password = PasswordField("Confirm new password:",
                                     render_kw={'placeholder': 'Please confirm your new password again'})

    submit = SubmitField('Confirm')


class ProcessForm(FlaskForm):
    '''For creating a new process'''
    theme=StringField("Theme:", validators=[DataRequired(), Length(0, 255)])
    level = SelectField("Level:", choices=[('Normal', 'Normal'), ('High', 'High')])
    contents=TextAreaField("Contents:",validators=[DataRequired()])
    submit=SubmitField('Submit')


