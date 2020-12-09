import json
import os
import sys

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils

# [register] [username] [password]
# password : 8 characters long

def write_json(data, filename='student-info/.student.json'): 
    '''
    Write given data to json file with specified filename. If
    filename isn't specified, data added to default json file,
    student.json

            Parameters:
                    data      (N/A): Data to be added to file
                    filename  (str): Json file's filename
    '''

    with open(filename,'w') as f: 
        json.dump(data, f, sort_keys=True, indent=4) 


def is_student_registered(registered_students, username):
    #TODO: write one function for login/register
    '''
    Checks whether student with specified username is registered by sorting through
    the given registered_students list

            Parameters:
                    registered_students (list of dict): List of registered students
                    username                     (str): Student's username

            Returns:
                    True  (boolean): Student's username and password exists in
                                     the registered_students list
                    False (boolean): Student's username and password does not 
                                     exist in the registered_students list
    '''

    for student in registered_students:
        if student['username'] == username:
            return True
    return False


def add_registration_info_to_json(user_info):
    #TODO: pass through username and password instead of whole dictionary
    '''
    Writes student's information (username and password) to the student.json file.

                Parameters:
                    user_info (dict): Information on student and given command
    '''

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
