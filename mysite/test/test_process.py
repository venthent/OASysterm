import unittest
from datetime import datetime
from mysite.app.models import Process,User
from mysite.app import creat_app, db



class LoginTest(unittest.TestCase):
    """Test auth view"""

    def setUp(self):
        self.app = creat_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        u=User(name='wangjie',password='1111')
        p = Process(theme='For Test', contents='This is a test process',user=u)
        db.session.add(u)
        db.session.add(p)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_process_is_not_none(self):
        p=Process.query.filter_by(theme='For Test').first()
        self.assertTrue(p is not None)

    def test_process_serial_num(self):
        p = Process.query.filter_by(theme='For Test').first()
        self.assertTrue(p.process_serial_num is not None)

    def test_what_process_serial_num_is(self):
        p = Process.query.filter_by(theme='For Test').first()
        self.assertTrue(p.process_serial_num=='WJ'+ datetime.utcnow().strftime('%Y%m%d%H%M%S'))

    def test_relationship_of_user(self):
        p = Process.query.filter_by(theme='For Test').first()
        self.assertTrue(p.user.name=='wangjie')




if __name__ == '__main__':
    unittest.main()
