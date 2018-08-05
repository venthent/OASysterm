from flask import Blueprint

# 创建登录蓝本
auth = Blueprint("auth", __name__)

from mysite.app.auth import views
