import os, sys, pickle, os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from urllib.request import urlopen
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils
from file_utils import find_home_directory


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 
            'https://www.googleapis.com/auth/calendar']


def create_service(username):
    '''
    Creates Google calendar API service and stores this information in 
    pickle file.This pickle file is user specific, username used to name
    file, and made secret.

            Parameters:
                    username (str): User specific username

            Returns:
                    service  (obj): Google calendar API service
    '''

    if username == 'codeclinic':
        directory = 'tokens/.'+username+'.pickle'
    else:
        directory = find_home_directory()+'/.'+username+'.pickle'
    creds = None
    check_calendar_connected()
    if os.path.exists(directory):
        with open(directory, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                print("ERROR: Major Error!")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0,
              success_message='You now have access to the codeclinic system!')
        # Save the credentials for the next run
        with open(directory, 'wb') as token:
            pickle.dump(creds, token)
    try:
        service = build('calendar', 'v3', credentials=creds)
    except Exception:
        utils.error_handling("ERROR: Calendar could not connect.")
    return service


def check_calendar_connected():
    '''
    Checks if internet is connected.

            Parameters:
                    username (str): User specific username
    '''
    
    try:
        response = urlopen('https://calendar.google.com/', timeout=10)
        connected = True
    except:
        connected = False
    if not connected:
        utils.error_handling("ERROR: No internet connection!")