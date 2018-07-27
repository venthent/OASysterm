import os

class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINISTRATOR='wangjie'
    DEBUG = True
    SSL_DISABLE = False

    @staticmethod
    def init_app(app):
        '''在这个方法中,可以执行对当前
环境的配置初始化'''
        pass

class Test(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL') or "mysql+pymysql://root:1111@localhost/OATEST"

class Dev(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or "mysql+pymysql://root:1111@localhost/OASYS"

config={
'default':Dev,
'test':Test,
}