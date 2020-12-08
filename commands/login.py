import json
import os
import sys
from datetime import datetime, timedelta

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils

# [login] [username] [password]
# password : 8 characters long


def log_in_expired(username):
    timestamp = ''
    now = datetime.now().strftime('%H:%M:%S')
    try:
        with open('data_files/.login_time.json', 'r') as json_file:
            info = json.load(json_file)
    except:
        utils.error_handling("ERROR: Please log-in with username and password.")
    if info:
        for student in info['expiration']:
            if student['username'] == username:
                timestamp = student['expire']
        if timestamp and timestamp < now:
            try:
                os.remove('tokens/.'+username+'.pickle')
            except:
                utils.error_handling("Something went wrong.")
            utils.error_handling("ERROR: Log-in time expired. Please log-in again!")
    else:
        utils.error_handling("ERROR: Log-in time expired. Please log-in again!")


def add_timestamps_to_json(username):
    half_an_hour_from_now = (datetime.now() + timedelta(hours=0.5)).strftime('%H:%M:%S')
    with open('data_files/.login_time.json', 'w') as json_file:
        pass
    try:
        if os.stat('data_files/.login_time.json').st_size == 0:
            info = {'expiration': [{'username': username, 'expire': half_an_hour_from_now}]}
            with open('data_files/.login_time.json', 'w') as f:
                json.dump(info, f, sort_keys=False, indent=4)
        else:
            index = -1
            with open('data_files/.login_time.json', 'r') as json_file:
                info = json.load(json_file)
            for i in range(len(info['expiration'])):
                if info['expiration'][i]['username'] == username:
                    index = i
            if index > -1:
                info['expiration'].pop(index)
            info['expiration'].append({'username': username, 'expire': half_an_hour_from_now})
            with open('data_files/.login_time.json', 'w') as f:
                json.dump(info, f, sort_keys=False, indent=4)
        return True
    except:
        return False
    

def is_valid_student_info(json_data, username, password):
    for student in json_data:
        if student['username'] == username and student['password'] == password:
            return True
    return False


def login_details(username, password):
    student_data = []
    if not os.stat('data_files/.student.json').st_size == 0:
        with open('data_files/.student.json') as json_file:
            student_data = json.load(json_file)
    if not student_data:
        utils.error_handling("INVALID: You are not registered! Register before logging in.")
    added = add_timestamps_to_json(username)
    if is_valid_student_info(student_data['student_info'], username, password) and added:
        utils.print_output("Login successful. Welcome to Code Clinic "+username+"!")
    else:
        utils.error_handling("ERROR: Incorrect username or password. Try again!")