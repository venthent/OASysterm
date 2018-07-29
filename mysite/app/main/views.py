from flask import url_for, render_template, flash, redirect, request
from flask_login import logout_user, login_user, login_required, current_user
from ..models import User, Process, Role
from mysite.app.main import main
from .forms import AccountForm, ProcessForm
from .. import db


# @main.route('/index')
@main.route('/index')
@login_required
def index():
    # page=request.args.get('page',default=1,type=int)

    process = Process.query.filter_by(approver=current_user._get_current_object().position).order_by(
        Process.timestamp.desc())
    return render_template('index.html', process=process)


@main.route('/sys/account/')  # 管理帐号
@login_required
def account_manage():
    per = current_user.role.permission
    if per == 'Administrator':
        users = User.query.order_by(User.id.asc()).all()
        return render_template('account_manage.html', permission=per, users=users)
    else:
        users = User.query.filter_by(id=current_user.id).all()
        return render_template('account_manage.html', permission=per, users=users)


@main.route('/sys/add', methods=['POST', 'GET'])
@login_required
def add_account():
    form = AccountForm()
    u = User.query.filter_by(name=form.name.data).first()
    if form.validate_on_submit():
        if u is None:
            new_user = User(name=form.name.data, real_name=form.real_name.data, password='1111',
                            position=form.position.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.account_manage'))
        flash('The Account name already exists,please try another one.')
        form.name.data = u.name
        form.real_name.data = u.real_name
        return render_template('add_account.html', form=form)
    else:
        return render_template('add_account.html', form=form)


@main.route('/sys/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_account(id):
    user = User.query.get_or_404(id)
    form = AccountForm()
    if form.validate_on_submit():
        if current_user == user:
            user.real_name = form.real_name.data
            if form.old_password.data.strip() != '' and form.new_password.data.strip() != '' and form.confirm_password.data.strip() != '':
                if user.verity_password(
                        form.old_password.data) and form.new_password.data == form.confirm_password.data:
                    user.password = form.new_password.data
                    flash('Password has been changed!')
                else:
                    flash('Password has not been changed!')
            if current_user.role.permission == 'Administrator':
                user.position = form.position.data
                r = Role(permission=form.permission.data)
                user.role = r
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.account_manage'))
        else:
            if current_user.role.permission == 'Administrator':
                user.real_name = form.real_name.data
                user.name = form.name.data
                user.real_name = form.real_name.data
                user.position = form.position.data
                r = Role(permission=form.permission.data)
                user.role = r
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.account_manage'))
    form.name.data = user.name
    form.real_name.data = user.real_name
    form.position.data = user.position  # Admin can see only
    form.permission.data = user.role.permission  # Admin can see only

    return render_template('edit_account.html', form=form, user=user)


@main.route('/StartProcess', methods=['POST', 'GET'])
@login_required
def start_process():
    form = ProcessForm()
    if form.validate_on_submit():
        theme = form.theme.data
        level = form.level.data
        contents = form.contents.data
        p = Process(theme=theme, contents=contents, level=level, user=current_user._get_current_object(),approver='Boss')
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('startprocess.html', form=form)
