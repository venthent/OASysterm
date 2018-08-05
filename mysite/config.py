import os,datetime

class Config:
    MY_PROCESS_PER_PAGE=10
    PROCCESS_PER_PAGE=10
    ACCOUNT_PER_PAGE=10
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
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