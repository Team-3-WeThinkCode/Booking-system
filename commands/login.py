import json
import os
import sys

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils

# from datetime import datetime

# [login] [username] [password]
# password : 8 characters long


def is_valid_student_info(json_data, username, password):
    for student in json_data:
        if student['username'] == username and student['password'] == password:
            return True
    return False


def login_details(user_info):
    with open('data_files/.student.json') as json_file:
        student_data = json.load(json_file)
        if is_valid_student_info(student_data['student_info'], user_info['username'], user_info['password']):
            utils.print_output("Login successful. Welcome to Code Clinic "+ user_info['username']+"!")
        else:
            utils.error_handling("Login details are not accurrate. Try again")