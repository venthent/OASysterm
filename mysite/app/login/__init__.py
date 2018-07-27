from flask import Blueprint

#创建登录蓝本
login = Blueprint("login", __name__)

from mysite.app.login import views
