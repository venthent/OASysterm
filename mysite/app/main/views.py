from datetime import datetime
from flask import url_for, render_template, flash, redirect, request, current_app
from flask_login import login_required, current_user
from ..models import User, Process, Role, Position, ProcessComments
from mysite.app.main import main
from .forms import EditAccount, ApprovalFrom, AddAccount
from .. import db


@main.route('/index')
@login_required
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Process.query.filter_by(next_approver=current_user._get_current_object().name,
                                         status='agree').order_by(
        Process.initial_time.desc()).paginate(page, per_page=current_app.config['PROCCESS_PER_PAGE'])
    process = pagination.items
    return render_template('index.html', process=process, pagination=pagination)


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
        process.timestamp = datetime.utcnow()
        process.status = form.agreement.data
        db.session.add(process)
        pc = ProcessComments(comments=form.comments.data, comments_status=form.agreement.data, process=process,
                             comments_author=current_user._get_current_object().name)
        db.session.add(pc)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('detail.html', process=process, form=form, next_users=next_users)


@main.route('/myprocess')
def myprocess():
    page = request.args.get('page', default=1, type=int)
    my_id = current_user.id
    pagination = Process.query.filter_by(user_id=my_id).order_by(Process.initial_time).paginate(page, per_page=
    current_app.config['MY_PROCESS_PER_PAGE'])
    myprocess = pagination.items
    return render_template('myprocess.html', myprocess=myprocess, pagination=pagination)


@main.route('/myprocess/detail/<int:id>')
def myprocess_detail(id):
    myprocess = Process.query.get(id)
    return render_template('myprocess_detail.html', myprocess=myprocess)


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
            return redirect(url_for("main.myprocess"))
        return render_template('startprocess.html', next_users=next_users)


@main.route('/sys/account/')  # 管理帐号
@login_required
def account_manage():
    page = request.args.get('page', 1, type=int)
    per = current_user.role.permission
    if per == 'Administrator':
        pagination = User.query.order_by(User.id.asc()).paginate(page, per_page=current_app.config['ACCOUNT_PER_PAGE'],
                                                                 error_out=False)
        users = pagination.items
    else:
        users = User.query.filter_by(id=current_user.id).all()
        pagination = None
    return render_template('account_manage.html', permission=per, users=users, pagination=pagination)


@main.route('/sys/add', methods=['GET', 'POST'])
@login_required
def add_account():
    form = AddAccount()
    if form.validate_on_submit():
        p = Position.query.filter_by(position_name=form.position.data).first()
        new_user = User(name=form.name.data, real_name=form.real_name.data, password='1111',
                        position=p)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.account_manage'))
    return render_template('add_account.html', form=form)


@main.route('/sys/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_account(id):
    user = User.query.get_or_404(id)
    form = EditAccount()
    p = Position.query.filter_by(position_name=form.position.data).first()
    r = Role.query.filter_by(permission=form.permission.data).first()
    if request.method=='POST':
        if current_user == user:
            user.real_name = form.real_name.data
            if form.check_password():
                if user.verity_password(form.old_password.data):
                    user.password = form.new_password.data
                    flash('Password has been changed!')
                else:
                    flash('Initial password is incorrect!')
            else:
                flash('Password has not been changed!')
            if current_user.role.permission == 'Administrator':
                if user.name != form.name.data and form.check_name():
                    user.name = form.name.data
                elif user.name != form.name.data:
                    flash('The Account name already exists,please try another one.')
                user.position = p
                user.role = r
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.account_manage'))
        else:
            if current_user.role.permission == 'Administrator':
                if user.name != form.name.data and form.check_name():
                    user.name = form.name.data
                elif user.name != form.name.data:
                    flash('The Account name already exists,please try another one.')
                user.real_name = form.real_name.data
                user.position = p
                user.role = r
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.account_manage'))
    form.name.data = user.name
    form.real_name.data = user.real_name
    form.position.data = user.position.position_name
    form.permission.data = user.role.permission
    return render_template('edit_account.html', form=form, user=user)


@main.route('/sys/delete/<int:id>')
def delete_account(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.account_manage'))
