import os, sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from utilities import utilities as utils
from utilities import file_utilities as file_utils


def is_student_registered(registered_students, username):
    '''
    Checks whether student with specified username is registered by sorting
    through the given registered_students list.

            Parameters:
                    registered_students (list of dict): List of registered
                                                        students
                    username                     (str): Student's username

            Returns:
                    True  (boolean): Student's username and password exists
                                     in the registered_students list
                    False (boolean): Student's username and password does
                                     not exist in the registered_students
                                     list
    '''

    for student in registered_students:
        if student['username'] == username:
            return True
    return False


def add_registration_info_to_json(username, password):
    '''
    Writes student's information (username and password) to the
    student.json file.

                Parameters:
                    username (str): Student's username
                    password (str): Student's password
    '''

    filename = 'student-info/.student.json'
    msg = ''
    if username == 'codeclinic':
        msg = 'ERROR: Invalid username.'
        utils.error_handling(msg)
    required_info = {'username': username, 'password': password}
    if os.stat(filename).st_size == 0:
        student_data = {'student_info' : []}
        student_data['student_info'].append(required_info)
        file_utils.write_data_to_json_file(filename, student_data)
    else:
        executed, student_data = file_utils.read_data_from_json_file(filename)
        if executed:
            if is_student_registered(student_data['student_info'], username):
                msg = "ERROR: You are already registered."
                utils.error_handling(msg)
            student_data['student_info'].append(required_info)
            file_utils.write_data_to_json_file(filename, student_data)
            msg = "Registration successful. Welcome to Code Clinic "+username+"!"
            utils.print_output(msg)
        else:
            msg = "ERROR: Could not register student."
            utils.error_handling(msg)
