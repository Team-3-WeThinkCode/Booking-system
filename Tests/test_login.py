import unittest
from unittest.main import main
from unittest.mock import patch
from io import StringIO
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import login
from utilities import file_utilities as file_utils


class Test(unittest.TestCase):
    def test_student_info(self):
        student_data = {'student_info': [{'password': 'password', 'username': 'cprinsloo'}, {'password': 'password', 'username': 'student'}, {'password': '12345678', 'username': 'sgerber'}, {'password': 'password', 'username': 'jroy'}, {'username': 'bnkala', 'password': 'Ad3laide'}]}
        self.assertTrue(login.is_valid_student_info(student_data['student_info'], 'jroy', 'password'))
        
    def test_student_not_valid(self):
        student_data = {'student_info': [{'password': 'password', 'username': 'cprinsloo'}, {'password': 'password', 'username': 'student'}, {'password': '12345678', 'username': 'sgerber'}, {'password': 'password', 'username': 'jroy'}, {'username': 'bnkala', 'password': 'Ad3laide'}]}
        self.assertFalse(login.is_valid_student_info(student_data['student_info'], 'Rhys', 'password'))

if __name__ == "__main__":
    unittest.main()