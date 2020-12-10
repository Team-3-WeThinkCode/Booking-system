from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
from utilities import split_username

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def create_email_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokens/.code_gmail.pickle'):
        with open('tokens/.code_gmail.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokens/.code_gmail.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service


def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {
    'raw': raw_message.decode("utf-8")
  }


def patient_create_text(username, event):
    message = f"""
Hello {split_username(event['attendees'][0]['email'])},
    
A user has booked your open slot:

Patient: {split_username(event['attendees'][1]['email'])}
Event date/time: {event['start']['dateTime'][:10]} \
{event['start']['dateTime'][11:16]}
Event ID: {event['id']}
User topic: {event['description']}

Please be aware that you are expected to attend this code clinic.
If you are unable to attend the meeting please contact the patient beforehand.

kind regards,
WeThinkCode_ Code-clinic.
    """
    return create_message("code.clinic.test@gmail.com",
                         event['attendees'][0]['email'],
                        "Code_Clinic booking made", message)
 


def patient_cancel_text(username, event):
    message = f"""
Hello {split_username(event['attendees'][0]['email'])},
    
A user has canceled a booking with you:

Event date/time: {event['start']['dateTime'][:10]} \
{event['start']['dateTime'][11:16]}
Event ID: {event['id']}

Please be aware that you are no longer expected to attend this code clinic.
If another booking is made in place of this slot, you will be notified.
    """
    return create_message("code.clinic.test@gmail.com",
                            event['attendees'][0]['email'],
                            "Code_Clinic booking canceled", message)


def send_message(user_id, message, service):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
"""
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
    except:
        print('An error occurred:')

