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
    '''
    Contacts google api services to create a service instance of the Gmail api.
    This will be used to send emails from the code clinic Gmail account.

            Parameters:
                    NONE

            Returns:
                    Service (obj): service object of Gmail instance
    '''
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
    '''
    Encode and format the message_text given for safe sending to the Gmail API 
    service, this is a requirement before sending emails.

            Parameters:
                    sender         (str): Email adress of sender
                    to             (str): Email address of recipient
                    subject        (str): Subject of email body
                    message_text   (str): Message body of the email

            Returns:
                    Email_body     (dict): Encoded bit file of email body
    '''
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
      'raw': raw_message.decode("utf-8")
    }


def patient_create_text(username, event):
    '''
    Create a email body to be used with the Gmail API, message will be created 
    and encoded in return. This message is for creating bookings

            Parameters:
                    username       (str): Username of patient
                    event          (obj): Current event object

            Returns:
                    Email_body     (dict): Encoded bit file of email body
    '''
    message = f"""
Hello {split_username(event['attendees'][0]['email'])},
    
A user has booked your open slot:

Patient: {username}
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
    '''
    Create a email body to be used with the Gmail API, message will be created 
    and encoded in return. This message is for canceling bookings

            Parameters:
                    username       (str): Username of patient
                    event          (obj): Current event object

            Returns:
                    Email_body     (dict): Encoded bit file of email body
    '''
    message = f"""
Hello {split_username(event['attendees'][0]['email'])},
    
A user has canceled a booking with you:

Patient: {username}
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
    '''
    Contacts the Gmail API service to send an email with the given email body

            Parameters:
                    service: (obj): Authorized Gmail API service instance.
                    user_id: (str): User's email address. The special value "me"
                                    can be used to indicate the authenticated user.
                    message: (obj): Message to be sent.        

            Returns:
                    NONE
    '''

    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
    except:
        print('An error occurred:')

