from flask import url_for, render_template, flash, redirect, request
from flask_login import logout_user, login_user, login_required, current_user
from ..models import User, Process, Role
from mysite.app.main import main
from .forms import AccountForm, ProcessForm
from .. import db

postion_list = ['Staff', 'Manager', 'Boss', ]


# @main.route('/index')
@main.route('/index')
@login_required
def index():
    # 既是首页，也是进行流程审批的页面
    # page=request.args.get('page',default=1,type=int)

    # 用数字1,2,3表示职位
    process = Process.query.filter_by(approver=current_user._get_current_object().position).order_by(
        Process.timestamp.desc())
    p = current_user.position
    if p is not 'Boss':
        pass
        # next_approver=postion_dict.get(postion_dict[p]+1)
    return render_template('index.html', process=process)


@main.route('/sys/account/')  # 管理帐号
@login_required
def account_manage():
    per = current_user.role.permission
    if per == 'Administrator':
        users = User.query.order_by(User.id.asc()).all()
    else:
        users = User.query.filter_by(id=current_user.id).all()
    return render_template('account_manage.html', permission=per, users=users)


@main.route('/sys/add', methods=['POST', 'GET'])
@login_required
def add_account():
    form = AccountForm()
    u = User.query.filter_by(name=form.name.data).first()
    if request.method == 'POST':
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
    if request.method == 'POST':
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
    next_users = None
    if current_user.position is not 'Boss':
        next_users = User.query.filter_by(position=(postion_list[postion_list.index(current_user.position) + 1])).all()

    if request.method == 'POST':
        pass

    return render_template('startprocess.html', next_users=next_users)
