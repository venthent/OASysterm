import os
from flask_script import Manager,Shell
from flask_migrate import MigrateCommand,Migrate
from mysite.app import db,creat_app
from mysite.app.models import User,Role,Process,Position

app=creat_app(config_name='default')
manager=Manager(app)
migrate=Migrate(app,db)
cwd=os.getcwd()

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Process=Process,Position=Position)

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    import unittest
    tests=unittest.TestLoader().discover(
        start_dir=os.path.join(cwd,'mysite/test'))
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__== '__main__':
    manager.run()
