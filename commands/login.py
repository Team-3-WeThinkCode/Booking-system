import os, sys, json
from datetime import datetime, timedelta

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils
import file_utils

# [login] [username] [password]
# password : 8 characters long


def log_in_expired(username):
    '''
    Confirms whether student's, with specified username, log-in time has expired 
    by retrieving the expiry date and time from the login_time.json file. This 
    date and time is compared to the current date and time. If log-in time has 
    expired, an error message is displayed.

            Parameters:
                    username  (str): Student's username
    '''

    timestamp, date = '', ''
    date_now = datetime.now().strftime('%y-%m-%d')
    time_now = time_now = datetime.now().strftime('%H:%M:%S')
    executed, info = file_utils.read_data_from_json_file('student-info/.login_time.json')
    if not executed:
        utils.error_handling("ERROR: Please log-in with username and password.")
    if info:
        for student in info['expiration']:
            if student['username'] == username:
                timestamp = student['time']
                date = student['date']
        if date and date < date_now:
            utils.error_handling("ERROR: Log-in time expired. Please log-in again!")
        elif timestamp and timestamp < time_now:
            try:
                os.remove(file_utils.find_home_directory()+'/.'+username+'.pickle')
            except:
                utils.error_handling("Something went wrong.")
            utils.error_handling("ERROR: Log-in time expired. Please log-in again!")
        elif not (date and timestamp):
            utils.error_handling("ERROR: Please log-in with username and password.")
    else:
        utils.error_handling("ERROR: Please log-in with username and password.")


def add_timestamps_to_json(username):
    '''
    Adds student's username, log-in expiry date and time to the login_time.json file
    as a list containing a dictionary. The expiry date/time is set to 4 hours from the
    current date/time.

            Parameters:
                    username  (str): Student's username
    '''

    expiry_date = (datetime.now() + timedelta(hours=4)).strftime('%y-%m-%d')
    expiry_time = (datetime.now() + timedelta(hours=4)).strftime('%H:%M:%S')
    try:
        if not file_utils.is_non_zero_file('student-info/.login_time.json'):
            with open('student-info/.login_time.json', 'w') as json_file:
                pass
            info = {'expiration': [{'username': username, 'date': expiry_date, 'time': expiry_time}]}
        else:
            index = -1
            executed, info = file_utils.read_data_from_json_file('student-info/.login_time.json')
            if not executed:
                return False
            for i in range(len(info['expiration'])):
                if info['expiration'][i]['username'] == username:
                    index = i
            if index > -1:
                info['expiration'].pop(index)
            info['expiration'].append({'username': username, 'date': expiry_date, 'time': expiry_time})
        file_utils.write_data_to_json_file('student-info/.login_time.json', info)
        return True
    except:
        return False
    

def is_valid_student_info(registered_students, username, password):
    '''
    Sorts through the registered_students list of registered students to confirm
    whether any student's information correlates with given information.

            Parameters:
                    registered_students (list of dict): List of registered students
                    username                     (str): Student's username
                    password                     (str): Student's password

            Returns:
                    True  (boolean): Student's username and password exists in
                                     the registered_students list
                    False (boolean): Student's username and password does not 
                                     exist in the registered_students list
    '''

    for student in registered_students:
        if student['username'] == username and student['password'] == password:
            return True
    return False


def login_details(username, password):
    '''
    Sorts through registered students from the student.json file and confirms
    whether student username and password is registered. If student is registered,
    student log-in expiry date and time is updated. If student is not registered,
    an error message is returned and program exits.

            Parameters:
                    username  (str): Student's username
                    password  (str): Student's password
    '''

    executed, student_data = file_utils.read_data_from_json_file('student-info/.student.json')
    if not executed:
        utils.error_handling("INVALID: You are not registered! Register before logging in.")
    if is_valid_student_info(student_data['student_info'], username, password):
        if add_timestamps_to_json(username):
            utils.print_output("Login successful. Welcome to Code Clinic "+username+"!")
        else:
            utils.error_handling("Something went wrong!")
    else:
        utils.error_handling("ERROR: Incorrect username or password. Try again!")