import json
import os
import sys

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils

# [register] [username] [password]
# campus : (CPT/JHB)
# password : 8 characters long

def write_json(data, filename='data_files/.student.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, sort_keys=True, indent=4) 


def is_student_registered(json_data, user_info):
    for student in json_data:
        if student['username'] == user_info['username']:
            return True
    return False


def add_registration_info_to_json(user_info):
    try:
        if os.stat('data_files/.student.json').st_size == 0:
            student_data = {'student_info' : []}
            student_data['student_info'].append(user_info)
            with open('data_files/.student.json', 'w') as f:
                json.dump(student_data, f, sort_keys=True, indent=4)
            utils.print_output("Registration successful! Welcome to Code Clinic "+ user_info['username']+".")
        else:
            with open('data_files/.student.json') as json_file: 
                student_data = json.load(json_file)
                if is_student_registered(student_data['student_info'], user_info):
                    utils.print_output("ERROR: You are already registered.")
                    return False
                temp = student_data['student_info']
                temp.append(user_info)
            write_json(student_data)
            utils.print_output("Registration successful! Welcome to Code Clinic "+ user_info['username']+".")
        return True
    except:
        utils.print_output('ERROR: Something went wrong! Try again.')
        return False
