import unittest
from unittest.main import main
from unittest.mock import patch
from io import StringIO
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import registration
# [register] [username] [password]
class Test(unittest.TestCase):

    def test_if_student_registered(self):
        user_info = {
    "student_info": [
        {
            "password": "password",
            "username": "cprinsloo"
        },
        {
            "password": "password",
            "username": "student"
        },
        {
            "password": "12345678",
            "username": "sgerber"
        },
        {
            "password": "password",
            "username": "jroy"
        }
    ]
        }
        self.assertTrue(registration.is_student_registered(user_info["student_info"], "jroy"))
        
    
    def test_student_not_registered(self):
        user_info = {
    "student_info": [
        {
            "password": "password",
            "username": "cprinsloo"
        },
        {
            "password": "password",
            "username": "student"
        },
        {
            "password": "12345678",
            "username": "sgerber"
        },
        {
            "password": "password",
            "username": "jroy"
        }
    ]
        }
        self.assertFalse(registration.is_student_registered(user_info['student_info'], 'bnkala'))

if __name__ == "__main__":
    unittest.main()