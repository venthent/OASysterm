from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    '''For Add account'''
    name = StringField("Account name:", validators=[DataRequired()], render_kw={'placeholder': 'Username,for login'})
    real_name = StringField("Real name:", validators=[DataRequired()])
    position = SelectField(label="Job position:",validators=[DataRequired()],
                           choices=[('Staff', 'Staff'), ('Manager', 'Manager'), ('Boss', 'Boss')])

    submit = SubmitField('Confirm')

class EditForm1(FlaskForm):
    '''For Add account while current_user is user and current_user's permission is Administrator'''
    name = StringField("Account name:", validators=[DataRequired()], render_kw={'placeholder': 'Username,for login'})
    real_name = StringField("Real name:", validators=[DataRequired()])
    position = SelectField(label="Job position:", validators=[DataRequired()],
                           choices=[('Staff', 'Staff'), ('Manager', 'Manager'), ('Boss', 'Boss')])
    permission = SelectField(label="Permission:", validators=[DataRequired()],
                             choices=[('Administrator', 'Administrator'), ('User', 'User')])

    old_password = PasswordField("Old password:", render_kw={
        'placeholder': 'If you write nothing,origional password will not be changed.'})
    new_password = PasswordField("New password:")
    confirm_password = PasswordField("Confirm new password:",
                                     render_kw={'placeholder': 'Please confirm your new password again'})
    submit = SubmitField('Confirm')

