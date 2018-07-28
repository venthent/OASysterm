from flask import url_for, render_template, flash, redirect, request
from flask_login import logout_user, login_user, login_required,current_user
from ..models import User,Process
from mysite.app.main import main
from .forms import AccountForm
from .. import db


#@main.route('/index')
@main.route('/index')
@login_required
def index():
    # page=request.args.get('page',default=1,type=int)

    process=Process.query.filter_by(approver=current_user._get_current_object().position).order_by(Process.timestamp.desc())
    return render_template('index.html',process=process)

@main.route('/sys/account/') #管理帐号
def account_manage():
    per=current_user.role.permission
    if per=='Administrator':
        users = User.query.order_by(User.id.asc()).all()
        return render_template('account_manage.html',permission=per,users=users)
    else:
        users=User.query.filter_by(id=current_user.id).all()
        return render_template('account_manage.html',permission=per,users=users)

@main.route('/sys/add',methods=['POST','GET'])
def add_account():
    form=AccountForm()
    if form.validate_on_submit():
        u=User.query.filter_by(name=form.name.data).first()
        if u is None:
            new_user=User(name=form.name.data,real_name=form.real_name.data,password='1111',position=form.position.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.account_manage'))
        flash('The Account name already exists,please try another one.')
        return redirect(url_for('main.add_account'))
    else:
        return render_template('add_account.html',form=form)
