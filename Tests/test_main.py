import unittest
from unittest import mock
import main

class Test(unittest.TestCase):


    def test_get_username_with_normal_string(self):
        original_input = mock.builtins.input
        mock.builtins.input = lambda _: 'student'
        self.assertEqual(main.get_username(), 'student')


    def test_get_username_with_string_with_integer(self):
        original_input = mock.builtins.input
        mock.builtins.input = lambda _: 'student3'
        self.assertEqual(main.get_username(), 'student3')


    def test_get_user_input_with_valid_input(self):
        original_input = mock.builtins.input
        mock.builtins.input = lambda _: '3'
        self.assertEqual(main.get_user_input(), 3)


    def test_get_user_input_with_invalid_input_then_valid_input(self):
        original_input = mock.builtins.input
        mock.builtins.input = lambda _: '0'
        mock.builtins.input = lambda _: '5'
        self.assertEqual(main.get_user_input(), 5)


if __name__ == "__main__":
    unittest.main()