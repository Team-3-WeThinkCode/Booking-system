import unittest
from unittest.main import main
from unittest.mock import patch
from io import StringIO
import sys
import os

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import login
import file_utils

class Test(unittest.TestCase):
    def test_student_info(self):
        filename='student-info/.student.json'
        executed, data = file_utils.read_data_from_json_file(filename)
        self.assertTrue(login.is_valid_student_info(data['student_info'], 'jroy', 'password'))
        

if __name__ == "__main__":
    unittest.main()