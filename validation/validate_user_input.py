import os, sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from utilities import utilities as utils
from utilities import file_utilities as file_utils


def is_registered(username):
    '''
    Checks whether student is registered by retrieving information from the
    ".student_info.json" and sorting through it to find the student's username.
    If username is not found, student is not registered.

            Parameters:
                    username  (str): Student's username

            Returns:
                    True  (boolean): Student is registered
                    False (boolean): Student is not registered             
    '''

    filename = 'student-info/.student.json'
    try:
        if not os.stat(filename).st_size == 0:
            executed, data = file_utils.read_data_from_json_file(filename)
            if executed:
                students = data['student_info']
                for student in students:
                    if student['username'] == username:
                        return True
    except FileNotFoundError:
        with open(filename, 'w') as json_file:
            pass
    return False


def contains_digit(arg):
    '''
    Confirms whether given argument contains a digit.  

            Parameters:
                    arg       (str): String to check
 
            Returns:
                    True  (boolean): String contains a digit 
                    False (boolean): String does not contain a digit        
    '''

    for letter in arg:
        if letter.isdigit():
            return True
    return False


def get_username(info):
    '''
    Sorts through the command-line arguments and finds username by filtering
    out commands and "main.py". The filtered list is iterated over to find
    the item of the list without a digit. This item is the username.

            Parameters:
                    info  (dict): Student information
 
            Returns:
                    info  (dict): Student information (includes username)      
    '''

    valid_args = ['create',
                  'cancel',
                  'register',
                  'volunteer',
                  'patient',
                  'list-bookings',
                  'list-open',
                  'list-slots',
                  'help',
                  '-h',
                  'login',
                  'format',
                  'export']
    lst_not_args = list(filter(lambda x: x not in valid_args, sys.argv))
    if lst_not_args:
        lst_command_arg = list(filter(lambda y: 'main.py' not in y, lst_not_args))
        for item in lst_command_arg:
            if not contains_digit(item):
                if (is_registered(item)) or 'register' in sys.argv:
                        info['username'] = item
                        return info
                else:
                    utils.error_handling('INVALID: You are not registered.')
        utils.error_handling('INVALID: Username not provided or invalid.')


def get_user_type(info):
    '''
    Sorts through the command-line arguments and checks whether user type
    (volunteer/patient) was specified. If user type is present, user type
    is added to the info dictionary

            Parameters:
                    info  (dict): Student information
 
            Returns:
                    info  (dict): Student information (includes user type) 
                    *     (list): Booleans that help to clarify which support 
                                  infomation is needed to execute command     
    '''

    get_date, get_time = False, False
    get_id, get_password = False, False
    if 'volunteer' in sys.argv:
        info['user_type'] = 'volunteer'
        get_date = True
        get_time = True
    if 'patient' in sys.argv:
        info['user_type'] = 'patient'
        get_id = True
    return info, [get_date, get_time, get_id, get_password]


def get_command(info, criteria):
    '''
    Sorts through the command-line arguments and finds command type 
    (create/cancel/list-bookings/list-open/list-slots/help/export) and 
    adds it to the info dictionary.

            Parameters:
                        info  (dict): Student information
                    criteria  (list): Booleans that help to clarify
                                      which support infomation is
                                      needed to execute command 
 
            Returns:
                    info  (dict): Student information
                                  (includes command type)   
    '''

    if 'create' in sys.argv:
        info['command'] = 'create'
    if 'cancel' in sys.argv:
        info['command'] = 'cancel'
    if 'list-bookings' in sys.argv:
        info['command'] = 'list-bookings'
    if 'list-slots' in sys.argv:
        info['command'] = 'list-slots'
    if 'list-open' in sys.argv:
        info['command'] = 'list-open'
        criteria[0] = True
    if sys.argv[1] == 'register':
        info['command'] = 'register'
        criteria[3] = True
    if sys.argv[1] == 'login':
        info['command'] = 'login'
        criteria[3] = True
    if 'export' in sys.argv:
        info['command'] = 'export'
    if '-h' in sys.argv or 'help' in sys.argv:
        info['command'] = 'help'
        if 'format' in sys.argv:
            info['command'] = 'format-help'
    return info


def get_support(info, criteria):
    '''
    Sorts through the command-line arguments and looks for support information
    (date/start time/UD/description/password) if program needs it to execute
    the given command. The list of booleans, criteria, is used to decide which
    support infomation is required.

            Parameters:
                        info  (dict): Student information
                    criteria  (list): Booleans that help to clarify which
                                      support infomation is needed to
                                      execute command 
 
            Returns:
                    True    (boolean): Required support information was given
                    info       (dict): Student information
                                       (includes support information)
    '''

    msg = ''
    get_date = criteria[0]
    get_time = criteria[1]
    get_id = criteria[2]
    get_password = criteria[3]
    if get_date:
        if len(sys.argv) >= 5 and utils.check_date_format(sys.argv[4]):
            info['date'] = sys.argv[4]
        elif len(sys.argv) == 4:
            if utils.check_date_format(sys.argv[3]):
                info['date'] = sys.argv[3]
            else:
                msg = 'INVALID: Date is either invalid or format is incorrect.\n'\
                                                  +'Enter date as <yyyy-mm-dd>'
                utils.error_handling(msg)
        else:
            msg = 'INVALID: Date is either invalid or format is incorrect.\n'\
                                                  +'Enter date as <yyyy-mm-dd>'
            utils.error_handling(msg)
    if get_time:
        if len(sys.argv) >= 6 and utils.check_time_format(sys.argv[5]):
            info['start_time'] = sys.argv[5]
        else:
            msg = 'ERROR: Time is either invalid or format is incorrect.\n'\
                                                +'Enter time in format <hh:mm>'
            utils.error_handling(msg)
    if get_id:
        info['UD'] = ''
        if 'command' in info and info['command'] == 'create':
            if len(sys.argv[-2]) == 26:
                info['UD'] = sys.argv[-2]
                info['description'] = sys.argv[-1]
                return info
        if len(sys.argv[len(sys.argv)-1]) == 26:
            info['UD'] = sys.argv[len(sys.argv)-1]
        return info
    if get_password:
        if len(sys.argv) == 4 and len(sys.argv[3]) == 8 and 'username' in info:
            info['password'] = sys.argv[3]
        else:
            msg = 'INVALID: Password needs to be at exactly 8 characters long.'
            utils.error_handling(msg)
    return info


def check_if_support_info_is_present(info):
    '''
    Sorts through the info dictionary and checks if all the information needed
    to execute command is present.

            Parameters:
                    info     (dict): Student information
 
            Returns:
                    True  (boolean): All required information is present
                                     in info dictionary
                    False (boolean): All required information is not
                                     present in info dictionary
    '''

    msg = ''
    if 'user_type' in info:
        is_user_type_command = (info['command'] == 'create' or info['command'] == 'cancel')
        if info['user_type'] == 'volunteer':
            date_passed = utils.date_has_passed(info['date'], info['start_time'])
            if ('date' in info and 'start_time' in info) and date_passed:
                msg = 'INVALID: Specified date/time has already passed.'
                utils.error_handling(msg)
            if 'date' in info and 'start_time' in info:
                if 'command' in info and is_user_type_command:
                    return True
            msg = 'INVALID: Enter command in format: '\
                +'<username> volunteer <command> <yyyy-mm-dd> <hh:mm>'
            utils.error_handling(msg)
        if info['user_type'] == 'patient':
            if 'UD' in info:
                if 'command' in info and is_user_type_command:
                    return True
            msg = 'INVALID: Enter command in format: '\
                    +'<username> patient <command> <event_id> <"description">'
            utils.error_handling(msg)
    elif 'command' in info:
        if info['command'] == 'list-open':
            if 'date' in info:
                return True
            msg = 'INVALID: Enter command in format: '\
                                          +'<username> list-open <yyyy-mm-dd>'
            utils.error_handling(msg)
        if info['command'] == 'register':
            if sys.argv[1] == 'register':
                if 'password' in info and 'username' in info:
                    return True
            msg = 'INVALID: Enter command in format: '\
                                +'register <username> <password>'
            utils.error_handling(msg)
        if info['command'] == 'login':
            if 'password' in info and 'username' in info:
                return True
            msg = 'INVALID: Enter command in format: '\
                            +'login <username> <password>'
            utils.error_handling(msg) 
        if not (info['command'] == 'cancel' or info['command'] == 'create'):
            return True
    return False


def get_user_commands():
    '''
    Collects required information from the command-line. If all required information
    is not present - the program will either print an error message to the terminal and exit
    or return an empty dictionary.
 
            Returns:
                    True     (boolean): All required information is present
                                        in info dictionary
                    False    (boolean): All required information is not
                                        present in info dictionary

                    info        (dict): Student information
                    *     (empty dict): Incorrect information provided by user
    '''

    info = get_username({})
    if info:
        info, criteria = get_user_type(info)
        info = get_command(info, criteria)
        info = get_support(info, criteria)
        if check_if_support_info_is_present(info):
            return True, info
        else:
            return False, {}
    return False, {}
