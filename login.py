import json

f = open('student.json',)
data = json.load(f)
f.close()

def get_username():
    username = input("Enter your username: ")
    for i in data['student_info']:
        if username in i['Username']:
            get_password()
        else:
            print("username not found")
            username = input("Enter your username: ")
            get_password()

    return username.lower()

def get_password():
    password = input("Enter your password :")
    for i in data['student_info']:
        if password in i['Password']:
            print("login successful")
        else :
            print("invalid user name/password!")
            get_password()
    return password.lower()


if __name__ == "__main__":
    get_username()
    