from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, SelectField, TextAreaField, ValidationError, RadioField
from wtforms.validators import DataRequired, Length, EqualTo
from ..models import User


class AddAccount(FlaskForm):
    name = StringField("Account name:", validators=[DataRequired(), Length(0, 20)],
                       render_kw={'placeholder': 'Username,for login'})
    real_name = StringField("Real name:", validators=[DataRequired()])
    position = SelectField(label="Job position:",
                           choices=[('Staff', 'Staff'), ('Manager', 'Manager'), ('Boss', 'Boss')])
    submit = SubmitField("Confirm")

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('The Account name already exists,please try another one.')


class EditAccount(FlaskForm):
    name = StringField("Account name:", validators=[DataRequired(), Length(0, 20)],
                       render_kw={'placeholder': 'Username,for login'})
    real_name = StringField("Real name:", validators=[DataRequired()])
    position = SelectField(label="Job position:",
                           choices=[('Staff', 'Staff'), ('Manager', 'Manager'), ('Boss', 'Boss')])

    permission = SelectField(label="Permission:",
                             choices=[('Administrator', 'Administrator'), ('User', 'User')])

    old_password = PasswordField("Old password:", render_kw={
        'placeholder': 'If you write nothing,origional password will not be changed.'})

    new_password = PasswordField("New password:",
                                 validators=[EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField("Confirm new password:",
                                     render_kw={'placeholder': 'Please confirm your new password again'})
    submit = SubmitField("Confirm")

    def check_name(self):
        if User.query.filter_by(name=self.name.data).first():
            return False
        return True

    def check_password(self):
        if self.old_password.data != '' and self.new_password.data != '' and\
                self.new_password.data == self.confirm_password.data:
            return True
        return False


class ProcessForm(FlaskForm):
    '''For creating a new process'''
    theme = StringField("Theme:", validators=[DataRequired(), Length(0, 255)])

    # 代表流程等级，" Normal"和" High"等级对应流程最终审批的职位
    level = SelectField("Level:", choices=[('Normal', 'Normal'), ('High', 'High')])
    contents = TextAreaField("Contents:", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ApprovalFrom(FlaskForm):
    comments = TextAreaField('Comments:', validators=[DataRequired()])
    agreement = RadioField('Agree?', choices=[('agree', 'Agree'), ('disagree', 'Disagree')])
    submit = SubmitField('Confirm')
