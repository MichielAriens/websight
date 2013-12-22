from api import *
import unittest

class TestUserAPI(unittest.TestCase):
    def test_user_validation2(self):
        create_user("testuser", "testpassword", "Mr. Test")
        self.assertTrue(validate_user("testuser", "testpassword"))
        self.assertFalse(validate_user("testuser", "jkfjlqsdjf"))


    def test_user_validation(self):
        try:
            create_user("testuser", "testpassword", "Mr. Test")
        except:
            pass       #user already exists
        self.assertTrue(validate_user("testuser", "testpassword"))
        self.assertFalse(validate_user("testuser", "jkfjlqsdjf"))




