import json
import os
import sys

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils

# [register] [username] [password]
# password : 8 characters long

def write_json(data, filename='student-info/.student.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, sort_keys=True, indent=4) 


def is_student_registered(json_data, username):
    for student in json_data:
        if student['username'] == username:
            return True
    return False


def add_registration_info_to_json(user_info):
    if user_info['username'] == 'codeclinic':
        utils.error_handling('ERROR: Invalid username.')
    required_info = {'username': user_info['username'], 'password': user_info['password']}
    if os.stat('student-info/.student.json').st_size == 0:
        student_data = {'student_info' : []}
        student_data['student_info'].append(required_info)
        with open('student-info/.student.json', 'w') as f:
            json.dump(student_data, f, sort_keys=True, indent=4)
    else:
        with open('student-info/.student.json') as json_file: 
            student_data = json.load(json_file)
            if is_student_registered(student_data['student_info'], user_info['username']):
                utils.error_handling("ERROR: You are already registered.")
            student_data['student_info'].append(required_info)
        write_json(student_data)
    utils.print_output("Registration successful. Welcome to Code Clinic "+ user_info['username']+"!")
