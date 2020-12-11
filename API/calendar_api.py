import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from urllib.request import urlopen
import utilities as utils
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar']

#TODO: Rename module

def create_service(username):
    '''
    Creates Google calendar API service and stores this information in pickle file.
    This pickle file is user specific, username used to name file, and made secret.

            Parameters:
                    username (str): User specific username

            Returns:
                    service  (obj): Google calendar API service
    '''

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