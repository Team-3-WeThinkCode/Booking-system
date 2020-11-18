import json
user_info = {}

def get_full_name():
    full_name = input("Enter your first name and surname: ")
    while full_name == '':
        full_name = input("Enter your first name and surname: ")
    return full_name

def get_username():
    username = input("Enter your username: ")
    while username == '':
        username = input("Enter your username: ")

    return username.lower()

def get_email_address(username):
    email_address = input("Enter your email address: ")
    while email_address == '':
        email_address = input("Enter your email address: ")

    while username != email_address.split('@')[0]:
        print('username not accurate')
        email_address = input("Enter your email address: ")
    
    return email_address

def get_campus():
    campus = input("Enter campus (Cape Town or Johannesburg): ")
    return campus

def get_password():

    password = input("Enter your password (minimum 8 characters): ")
    while password == '':
        password = input("Enter your password (minimum 8 characters): ")
    while len(password) < 8:
        print("Password too short")
        password = input("Enter your password (minimum 8 characters):")
   
    return password

def validate_password(password):
    check_password = input("Re-enter password: ")
    while check_password != password:
        print("Password is not the same")
        check_password = input("Re-enter password: ")
    
    return check_password

if __name__  == "__main__":
    name = get_full_name()
    username = get_username()
    email = get_email_address(username)
    print(email.split('@')[0])
    password = get_password()
    check_password = validate_password(password)
    print("Registration successful! Welcome to Code Clinic "+ username+".")