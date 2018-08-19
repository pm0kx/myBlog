import unittest

from app.common.mails import send_mail
from app.common.db import db
from app import create_app
from app.models import User


class TestSendMails(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.to='709631358@qq.com'

    @classmethod
    def tearDownClass(cls):
        pass

    def test_1_send(self):
        user1 = User()
        user1.username='test'
        send_mail('Confirm Your Account',self.to)

if __name__ == '__main__':
    unittest.main()
