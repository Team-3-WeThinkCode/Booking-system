import json
import os
import sys

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
                temp.append(student_info)
            write_json(student_data)
        return True, "Registration successful! Welcome to Code Clinic "+ student_info['username']+"."
    except:
        return False, 'Something went wrong! Try again.'


def validate_password(password):
    if not len(password) == 9:
        return False
    return True


def validate_campus(campus):
    if campus == 'Cape Town' or campus == 'Johannesburg':
        return True
    return False


def get_student_info():
    student_info = {'username': sys.argv[1]}
    if not ('register' in sys.argv or len(sys.argv) == 5):
        return {}
    student_info['password'] = sys.argv[4]
    if 'CPT' in sys.argv:
        student_info['campus'] = 'Cape Town'
    elif 'JHB' in sys.argv:
        student_info['campus'] = 'Johannesburg'
    else:
        return {}
    student_info['email'] = student_info['username'] + '@student.wethinkcode.co.za'
    return student_info


def validate_registration_info(info):
    '''
    if 'register' in info and 'name' in info and 'password' in info and 'campus' in info:
        adding_details(info['username'], info['password'], info['campus'])
    '''
    if info:
        if not validate_password(info['password']):
            print('INVALID INPUT: Please enter password with length of 9.')
            return False
        if not validate_campus(info['campus']):
            print('INVALID INPUT: Please enter valid campus (JHB/CPT).')
            return False
        return True
    else:
        print('INVALID INPUT')
        return False


if __name__  == "__main__":
    #[username] [register] [campus] [password]
    student_info = get_student_info()
    if validate_registration_info(student_info):
        added, output = add_info_to_json(student_info)
        print(output)
