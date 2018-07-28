from flask import Blueprint

main=Blueprint("main",__name__)

from mysite.app.main import views
