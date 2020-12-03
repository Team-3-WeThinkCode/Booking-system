import sys
import utilities as utils


def get_username(info):
    '''
    Gets username from command line arguments and adds it to the given dictionary
    :return: Dictionary with username if username in command line arguments
    :return: Empty dictionary if username was not in command line arguments
    '''

    valid_args = ['create', 'cancel', 'volunteer', 'patient', 'list-bookings', 'list-open', 'list-slots']
    lst_not_args = list(filter(lambda x: x not in valid_args, sys.argv))
    if lst_not_args:
        lst_username = list(filter(lambda y: y != 'main.py', lst_not_args))
        for item in lst_username:
            if not (('/' in item) or ('-' in item) or (':' in item)) and len(item)==9:
                info['username'] = item
                return info
    return {}


def get_user_type(info):
    '''
    Gets user type (volunteer/patient) from command line arguments and adds
    it to the given dictionary
    :return: Dictionary with user type if user type specified in command line arguments
    :return: Given dictionary if user type was not specified in command line arguments
    '''

    get_date, get_time, get_id = False, False, False
    if 'volunteer' in sys.argv:
        info['user_type'] = 'volunteer'
        get_date = True
        get_time = True
    if 'patient' in sys.argv:
        info['user_type'] = 'patient'
        get_id = True
    return info, [get_date, get_time, get_id]


def get_command(info, criteria):
    '''
    Gets command type (create/cancel/list-bookings/list-open/list-slots) from command line
    arguments and adds it to the given dictionary
    :return: Dictionary with command if command specified in command line arguments
    :return: Given dictionary if command was not specified in command line arguments
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
    return info


def get_support(info, criteria):
    '''
    Gets support args (date/time/calendar id) from command line arguments and adds it
    to the given dictionary
    :return: Dictionary with support args if specified in command line arguments
    :return: Given dictionary if support args was not specified in command line arguments
    '''

    get_date, get_time, get_id = criteria[0], criteria[1], criteria[2]
    if get_date:
        if len(sys.argv) >= 5 and utils.check_date_format(sys.argv[4]):
            info['date'] = sys.argv[4]
        elif len(sys.argv) == 4 and utils.check_date_format(sys.argv[3]):
            info['date'] = sys.argv[3]
        else:
            return False, info
    if get_time:
        if len(sys.argv) >= 6 and utils.check_time_format(sys.argv[5]):
            info['start_time'] = sys.argv[5]
        else:
            return False, info
    if 'date' in info and 'time' in info:
        if utils.date_has_passed(info['date'], info['time']):
            return False, info
    if get_id:
        info['UD'] = ''
        if len(sys.argv[len(sys.argv)-1]) == 26:
            info['UD'] = sys.argv[len(sys.argv)-1]
            return True, info
    return True, info


def check_if_support_info_is_present(info):
    '''
    Confirms whether required information was given for the program to execute command
    :return: True if required information was given
    :return: False if required information was not given
    '''

    if 'user_type' in info:
        if info['user_type'] == 'volunteer':
            if 'date' in info and 'start_time' in info:
                if 'command' in info and (info['command'] == 'create' or info['command'] == 'cancel'):
                    return True
            return False
        if info['user_type'] == 'patient':
            if 'UD' in info:
                if 'command' in info and (info['command'] == 'create' or info['command'] == 'cancel'):
                    return True
            return False
    elif 'command' in info:
        if info['command'] == 'list-open':
            if 'date' in info:
                return True
            return False
    return True


def get_user_commands():
    '''
    Collects required information for the program to execute expected command
    :return: True if valid information was collected; Dictionary with required information
    :return: False if invalid information was collected; Empty Dictionary
    '''

    info = get_username({})
    if info:
        info, criteria = get_user_type(info)
        info = get_command(info, criteria)
        valid_format, info = get_support(info, criteria)
        if valid_format and check_if_support_info_is_present(info):
            return True, info
        else:
            return False, {}
    return False, {}