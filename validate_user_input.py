import sys
import utilities as utils


def get_user_type(info):
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
    get_date, get_time, get_id = criteria[0], criteria[1], criteria[2]
    if get_date:
        if len(sys.argv) >= 5 and utils.check_date_format(sys.argv[4]):
            info['date'] = sys.argv[4]
        elif len(sys.argv) == 4 and utils.check_date_format(sys.argv[3]):
            info['date'] = sys.argv[3]
        else:
            return False, info,'INVALID: Enter date in correct format.'
    if get_time:
        if len(sys.argv) >= 6 and utils.check_time_format(sys.argv[5]):
            info['start_time'] = sys.argv[5]
        else:
            return False, info, 'INVALID: Enter time in correct format.'
    if 'date' in info and 'time' in info:
        if utils.date_has_passed(info['date'], info['time']):
            return False, info, "INVALID: Date/time has already passed."
    if get_id:
        if len(sys.argv[len(sys.argv)-1]) == 26:
            info['UD'] = sys.argv[len(sys.argv)-1]
        else:
            return False, info, "INVALID: Enter valid ID."
    return True, info, ""


def check_if_support_info_is_present(info):
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
    info, criteria = get_user_type({})
    info = get_command(info, criteria)
    valid_format, info, output = get_support(info, criteria)
    if valid_format and check_if_support_info_is_present(info):
        return True, info
    else:
        print(output)
        return False, {}


if __name__ == "__main__":
    valid, info = get_user_commands()
    print(info)