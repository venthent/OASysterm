from flask import url_for,render_template,flash,redirect,request
from flask_login import logout_user,login_user,login_required
from .login_form import LoginForm
from ..models import User
from mysite.app.login import auth

@auth.route('/login',methods=['POST','GET'])
def login():
    loginform=LoginForm()
    if loginform.validate_on_submit():
        user=User.query.filter_by(name=loginform.name.data).first()
        if user is not None and user.verity_password(loginform.password.data):
            login_user(user=user,remember=loginform.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(message='Invalid username or password!')
    return render_template('login.html',form=loginform)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logout')
    return redirect(url_for('auth.login'))



