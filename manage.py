import random
import os
from datetime import timedelta
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate
from mysite.app import db, creat_app
from mysite.app.models import User, Role, Process, Position

app = creat_app(config_name='default')
app.permanent_session_lifetime = timedelta(minutes=10)
#this is a test from wangjie
#hello
manager = Manager(app)
migrate = Migrate(app, db)
cwd = os.getcwd()


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Process=Process, Position=Position)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover(
        start_dir=os.path.join(cwd, 'mysite/test'))
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    from  flask_migrate import upgrade
    from mysite.app.models import User,Role, Position

    upgrade()
    #this is a upgrade
    #deploy
    Role.insert_roles()
    Position.insert_positions()
    User.insert_administrator()


if __name__ == '__main__':
    manager.run()
