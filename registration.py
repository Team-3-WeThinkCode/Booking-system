import json
import os
import sys

"""
def get_full_name():
    '''
    This will ask the user to enter his or her first name and surname
    Return the first name and surname as the first name as the full name.
    '''
    full_name = input("Enter your first name and surname: ")
    while full_name == '':
        full_name = input("Enter your first name and surname: ")

    
    return full_name

def get_username():
    '''
    This will prompt the user to enter the username
    '''
    username = input("Enter your username: ")
    while username == '':
        username = input("Enter your username: ")
    username = username.lower()
    # user_info['username'] = username
    return username

def get_email_address(username):
    '''
    This will prompt the user to enter the email address, it will check if the name is exactly the same as the username
    and will also check if the domain is 'student.wethinkcode.co.za', otherwise the user must re-enter the email address
    '''
    email_address = input("Enter your email address: ")
    while email_address == '':
        email_address = input("Enter your email address: ")
    
    while username != email_address.split('@')[0]:
        print('username not accurate')
        email_address = input("Enter your email address: ")
    
    while email_address.split('@')[1].lower() != 'student.wethinkcode.co.za':
        print('email domain not accurate')
        email_address = input("Enter your email address: ")
    # user_info['email address'] = email_address
    return email_address

def get_campus():
    campus = input("Enter campus (Cape Town or Johannesburg): ")
    
    return campus

def get_password():
    '''
    This will prompt the user to check the password entered is 8 characters in length or longer
    Otherwise the user must re-enter the password
    '''

    password = input("Enter your password (minimum 8 characters): ")
    while password == '':
        password = input("Enter your password (minimum 8 characters): ")
    while len(password) < 8:
        print("Password too short")
        password = input("Enter your password (minimum 8 characters):")
    # user_info['password'] = password
    return password

def validate_password(password):
    '''
    This will validate whether the password entered is exactly the same as the original one entered.
    '''
    check_password = input("Re-enter password: ")
    while check_password != password:
        print("Password is not the same")
        check_password = input("Re-enter password: ")
    
    return check_password

def adding_details(username, password, campus):
    #don't think we need a full name??; validate info??
    '''
    name = get_full_name()
    username = get_username()
    email = get_email_address(username)
    campus = get_campus()
    password = get_password()
    check_password = validate_password(password)
    '''
    user_info = {"Username": username, 
    "Email": username+'@student.wethinkcode.co.za',
    "Campus": campus, 
    "Password": password}
    student_data = {"student_info": []}
    with open("student.json") as json_file:
        student_data = json.load(json_file)
        temp = student_data['student_info']
        y = user_info
        temp.append(y)   
    # student_data['student_info'].append(user_info)
    with open("student.json", "w") as outfile:
         json.dump(student_data, outfile, indent=4)
    print("Registration successful! Welcome to Code Clinic "+ username+".")
"""

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
    #[username] [registration] [campus] [password]
    student_info = get_student_info()
    if validate_registration_info(student_info):
        added, output = add_info_to_json(student_info)
        print(output)
