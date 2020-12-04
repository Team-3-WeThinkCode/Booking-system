import json
import os
import sys

#[register] [username] [password]
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
        else:
            with open('data_files/.student.json') as json_file: 
                student_data = json.load(json_file)
                if is_student_registered(student_data['student_info'], user_info):
                    return False, "You're already registered."
                temp = student_data['student_info']
                temp.append(user_info)
            write_json(student_data)
        return True, "Registration successful! Welcome to Code Clinic "+ user_info['username']+"."
    except:
        return False, 'ERROR: Something went wrong! Try again.'
