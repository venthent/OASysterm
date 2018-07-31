from datetime import datetime
from . import db
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    real_name = db.Column(db.String(20), default=None)
    password_hash = db.Column(db.String(128))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    process = db.relationship('Process', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        '''大多数用户在注册时赋予的角色都是默认角色“User”,“Administrator”由设置变量 ADMINISTRATOR 识别'''
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.name == current_app.config['ADMINISTRATOR']:
                self.role = Role.query.filter_by(permission='Administrator').first()
            else:
                self.role = Role.query.filter_by(permission='User').first()

    @property
    def password(self):
        # 不允许读取 password 属性的值
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        '''生成password的哈希值'''
        self.password_hash = generate_password_hash(password)

    def verity_password(self, password):
        '''接 受 一 个 参 数( 即 密 码 ), 将 其 传 给  check_password_hash() 函数,
        和password_hash进行比对。如果返回True ,就表明密码是正确的'''
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', backref='role', lazy='dynamic')
    permission = db.Column(db.String(20))

    @staticmethod
    def insert_roles():
        '''将角色自动添加到数据库中'''
        roles = ['Administrator', 'User', ]

        for r in roles:
            role = Role.query.filter_by(permission=r).first()
            if role is None:
                role = Role(permission=r)
            db.session.add(role)
        db.session.commit()


# 职位,分别为'Staff','Manager','Boss'
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', backref='position', lazy='dynamic')
    position_name = db.Column(db.String(20))

    @staticmethod
    def insert_positions():
        '''将职位自动添加到数据库中'''
        positions = ['Staff', 'Manager', 'Boss', ]
        for p in positions:
            position = Position.query.filter_by(position_name=p).first()
            if position is None:
                position = Position(position_name=p)
            db.session.add(position)
        db.session.commit()


class Process(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(256))
    contents = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    initial_time=db.Column(db.DateTime,default=datetime.utcnow)
    # 下一个审批人的名字,'None'表示走到尽头,审批完成
    next_approver = db.Column(db.String(20), default=None)
    process_serial_num = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # level:High,Normal
    level = db.Column(db.String(20))
    status = db.Column(db.String(12),default='agree')
    process_coments = db.relationship('ProcessComments', backref='process', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Process, self).__init__(**kwargs)
        if self.process_serial_num is None:
            self.process_serial_num = 'WJ' + datetime.utcnow().strftime('%Y%m%d%H%M%S')


class ProcessComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.Text)
    process_id = db.Column(db.Integer, db.ForeignKey('process.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
