import os, sys, unittest
from unittest.main import main
from unittest.mock import patch
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import registration
from utilities import file_utilities as file_utils


class Test(unittest.TestCase):

    def test_if_student_registered(self):
        student_data = {'student_info': [{'password': 'password', 'username': 'cprinsloo'}, {'password': 'password', 'username': 'student'}, {'password': '12345678', 'username': 'sgerber'}, {'password': 'password', 'username': 'jroy'}, {'username': 'bnkala', 'password': 'Ad3laide'}]}
        self.assertTrue(registration.is_student_registered(student_data['student_info'], 'jroy'))
    
    def test_student_not_registered(self):
        student_data = {'student_info': [{'password': 'password', 'username': 'cprinsloo'}, {'password': 'password', 'username': 'student'}, {'password': '12345678', 'username': 'sgerber'}]}
        self.assertFalse(registration.is_student_registered(student_data['student_info'], 'bnkala'))

if __name__ == "__main__":
    unittest.main()