import unittest
from unittest.main import main
from unittest.mock import patch
from io import StringIO
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import login

class Test(unittest.TestCase):
    def test_login(self):
        pass

if __name__ == "__main__":
    unittest.main()