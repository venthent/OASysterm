from flask import url_for, render_template, flash, redirect, request
from flask_login import logout_user, login_user, login_required
from ..models import User
from mysite.app.main import main


@main.route('/index')
@main.route('/')
@login_required
def index():
    # page=request.args.get('page',default=1,type=int)
    return render_template('index.html')
