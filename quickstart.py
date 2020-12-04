from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from urllib.request import urlopen
import utilities as utils
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar']
#service = None


def create_service(username):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    
    
    check_calendar_connected()
    if os.path.exists('tokens/.'+username+'.pickle'):
        with open('tokens/.'+username+'.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request()) # TODO #1: Add exception handling here (and really the entire block) to capture authentication/authorization issues
            except:
                print("ERROR: Major Error!")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0, success_message='You now have access to the codeclinic system!')
        # Save the credentials for the next run
        with open('tokens/.'+username+'.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('calendar', 'v3', credentials=creds) #Add exception handling here to capture client side issues
    except Exception:
        utils.print_output("ERROR: Calendar could not connect.")
    return service

def internet_on():
    '''
    Function checks if internet is connected and returns False if it isn't.
    '''
    try:
        response = urlopen('https://calendar.google.com/', timeout=10)
        return True
    except: 
        return False

'''TODO Check connection to Google Calendar succesfull (maybe check pickle file)'''
def check_calendar_connected():
    '''
    Calls the internet_on() function and then prints "no internet" if check equals False.
    '''
    check = internet_on()
    if check == False:
        utils.print_output("ERROR: No internet connection!")