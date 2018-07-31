from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, SelectField,TextAreaField,ValidationError
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


#
    submit = SubmitField("Commit")

    def validate_name(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('The Account name already exists,please try another one.')


class ProcessForm(FlaskForm):
    '''For creating a new process'''
    theme=StringField("Theme:", validators=[DataRequired(), Length(0, 255)])

    # 代表流程等级，" Normal"和" High"等级对应流程最终审批的职位
    level = SelectField("Level:", choices=[('Normal', 'Normal'), ('High', 'High')])
    contents=TextAreaField("Contents:",validators=[DataRequired()])
    submit=SubmitField('Submit')


