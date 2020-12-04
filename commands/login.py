import json
from datetime import datetime

# user_info= open('data_files/.student.json', 'r')
# user_data = json.load(user_info)

# def write_json(data, filename= '.timestamp.json'):
#     with open(filename, 'w') as f:
#         json.dump(data, f, sort_keys= True, indent=4)

# def user_login(user_info):
#     with open('data_files/.student.json') as json_file:
#         student_data = json.load(json_file)
#         for student in student_data:
#             if student['username'] == user_info['username'] and student['password'] == user_info['password']:

def get_username():
    return input("Enter your username: ")

def get_password():
    return input("Enter your password: ")

# def login_details():
#     with open('data_files/.student.json') as json_file:
#         student_data = json.lo