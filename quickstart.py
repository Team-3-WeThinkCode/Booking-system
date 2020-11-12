from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar']
#service = None

def create_service(username):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    
    if os.path.exists('tokens/.'+username+'.pickle'):
        with open('tokens/.'+username+'.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request()) # TODO #1: Add exception handling here (and really the entire block) to capture authentication/authorization issues
            except:
                print("Major Error!")
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
        print("Error")
    return service

'''TODO Check connection to Google Calendar succesfull (maybe check pickle file)'''
def check_calendar_connected():
    pass