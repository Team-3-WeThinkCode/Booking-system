import json
import os
import sys

#[username] [register] [campus] [password]
# campus : (CPT/JHB)
# password : 9 characters long

def write_json(data, filename='data_files/.student.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, sort_keys=True, indent=4) 


def is_student_registered(json_data, user_info):
    for student in json_data:
        if student['username'] == user_info['username']:
            return True
    return False


def add_info_to_json(user_info):
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


def validate_password(password):
    if not len(password) == 9:
        return False
    return True


def validate_campus(campus):
    if campus == 'Cape Town' or campus == 'Johannesburg':
        return True
    return False


def validate_registration_info(info):
    '''
    if 'register' in info and 'name' in info and 'password' in info and 'campus' in info:
        adding_details(info['username'], info['password'], info['campus'])
    '''
    if info:
        if not validate_password(info['password']):
            utils.print_output('INVALID: Please enter password with length of 9.')
            return False
        if not validate_campus(info['campus']):
            utils.print_output('INVALID: Please enter valid campus (JHB/CPT).')
            return False
        return True
    else:
        utils.print_output('INVALID: Registration information entered incorrectly.\nUse the help command for the correct format.\nHelp command: [username] [-h]')
        return False
