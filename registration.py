import json
user_info = {}
j = json.dumps(user_info)
def get_full_name(user_info, j):
    '''
    This will ask the user to enter his or her first name and surname
    Return the first name and surname as the first name as the full name.
    '''
    full_name = input("Enter your first name and surname: ")
    while full_name == '':
        full_name = input("Enter your first name and surname: ")
    user_info['name'] = full_name
    
    return full_name

def get_username(user_info, j):
    '''
    This will prompt the user to enter the username
    '''
    username = input("Enter your username: ")
    while username == '':
        username = input("Enter your username: ")
    username = username.lower()
    user_info['username'] = username
    return username

def get_email_address(username, user_info, j):
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
    user_info['email address'] = email_address
    return email_address

# def get_campus():
#     campus = input("Enter campus (Cape Town or Johannesburg): ")
#     return campus

def get_password(user_info, j):
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
    user_info['password'] = password
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

if __name__  == "__main__":
    name = get_full_name(user_info, j)
    username = get_username(user_info, j)
    email = get_email_address(username, user_info, j)
    password = get_password(user_info, j)
    check_password = validate_password(password)
    print(user_info)
    print(j)
    print("Registration successful! Welcome to Code Clinic "+ username+".")