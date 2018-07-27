import unittest
from mysite.app.models import User
from mysite.app import creat_app,db


class LoginTest(unittest.TestCase):
    """Test login view"""
    def setUp(self):
        self.app=creat_app('test')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()
        user=User(name='wangjie',password='1111')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user(self):
        u=User.query.get(1)
        self.assertTrue(u is not None)
if __name__=='__main__':
    unittest.main()