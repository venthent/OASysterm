from datetime import datetime
from flask import url_for, render_template, flash, redirect, request
from flask_login import logout_user, login_user, login_required, current_user
from ..models import User, Process, Role, Position, ProcessComments
from mysite.app.main import main
from .forms import AccountForm, ProcessForm, ApprovalFrom
from .. import db

postion_list = ['Staff', 'Manager', 'Boss', ]


@main.route('/index')
@login_required
def index():
    # page=request.args.get('page',default=1,type=int)
    process = Process.query.filter_by(next_approver=current_user._get_current_object().name, status='agree').order_by(
        Process.initial_time.desc())
    return render_template('index.html', process=process)


# 详情页面，并进行流程审批
@main.route('/index/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    form = ApprovalFrom()
    process = Process.query.get(id)
    level = process.level
    next_users = None
    if current_user._get_current_object().position.position_name != 'Boss':
        if level == 'High':
            next_users = User.query.filter_by(position=Position.query.get(current_user.position.id + 1)).all()
    if form.validate_on_submit():
        if next_users:
            process.next_approver = request.form.get("nextname")
        else:
            process.next_approver = None
        process.status = form.agreement.data
        process.timestamp = datetime.utcnow()
        db.session.add(process)
        pc = ProcessComments(comments=form.comments.data, process=process)
        db.session.add(pc)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('detail.html', process=process, form=form, next_users=next_users)


@main.route('/sys/account/')  # 管理帐号
@login_required
def account_manage():
    per = current_user.role.permission
    if per == 'Administrator':
        users = User.query.order_by(User.id.asc()).all()
    else:
        users = User.query.filter_by(id=current_user.id).all()
    return render_template('account_manage.html', permission=per, users=users)


@main.route('/sys/add', methods=['GET', 'POST'])
@login_required
def add_account():
    form = AccountForm()
    u = User.query.filter_by(name=form.name.data).first()
    if request.method == 'POST':
        if u is None:
            p = Position.query.filter_by(position_name=form.position.data).first()
            new_user = User(name=form.name.data, real_name=form.real_name.data, password='1111',
                            position=p)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.account_manage'))
        flash('The Account name already exists,please try another one.')
        form.name.data = u.name
        form.real_name.data = u.real_name
        return render_template('add_account.html', form=form)
    return render_template('add_account.html', form=form)


# have bugs
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
                user.position.position_name = form.position.data
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
                user.position.position_name = form.position.data
                r = Role(permission=form.permission.data)
                user.role = r
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.account_manage'))
    form.name.data = user.name
    form.real_name.data = user.real_name
    form.position.data = user.position.position_name  # Admin can see only
    form.permission.data = user.role.permission  # Admin can see only

    return render_template('edit_account.html', form=form, user=user)


@main.route('/StartProcess', methods=['POST', 'GET'])
@login_required
def start_process():
    next_users = None
    # id=3 de jiushi Boss
    current_user_position_id = current_user.position.id
    if current_user_position_id < 3:
        next_users = User.query.filter_by(position=Position.query.get(current_user_position_id + 1)).all()
    if next_users is None:
        flash("You need not create process!")
        return redirect(url_for("main.index"))
    else:
        if request.method == 'POST':
            process = Process(theme=request.form.get("theme"), contents=request.form.get("contents"),
                              next_approver=request.form.get("nextname"), level=request.form.get("level"),
                              user=current_user._get_current_object())
            db.session.add(process)
            db.session.commit()
            return redirect(url_for("main.index"))
        return render_template('startprocess.html', next_users=next_users)
