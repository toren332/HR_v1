from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def connect_google_api():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('google_calendar/token.pickle'):
        with open('google_calendar/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_calendar/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('google_calendar/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)


def get_calendar_id(calendar_name: str) -> str:
    service = connect_google_api()
    calendar_list = service.calendarList().list(pageToken=None).execute()
    for calendar_list_entry in calendar_list['items']:
        if str(calendar_list_entry['summary']) == calendar_name:
            return calendar_list_entry['id']
    raise AssertionError('there is no calendar with this name')


def create_calendar(calendar_name: str) -> str:
    service = connect_google_api()
    calendar_list = service.calendarList().list(pageToken=None).execute()
    for calendar_list_entry in calendar_list['items']:
        if str(calendar_list_entry['summary']) == calendar_name:
            raise AssertionError('calendar with this name already exist')

    calendar = {
        'summary': calendar_name,
        'timeZone': 'Europe/Moscow'
    }
    return service.calendars().insert(body=calendar).execute()['id']


def get_or_create_calendar(calendar_name: str) -> str:
    service = connect_google_api()
    calendar_list = service.calendarList().list(pageToken=None).execute()
    for calendar_list_entry in calendar_list['items']:
        if str(calendar_list_entry['summary']) == calendar_name:
            return calendar_list_entry['id']

    calendar = {
        'summary': calendar_name,
        'timeZone': 'Europe/Moscow'
    }
    return service.calendars().insert(body=calendar).execute()['id']


def create_event(calendar_name: str, event_name: str, location: str, description: str,
                 start_time: datetime.datetime, end_time: datetime.datetime, recurrence=None):
    service = connect_google_api()
    event = {
        'summary': event_name,
        'location': location,
        'description': description,
        'start': {
            'dateTime': str(start_time.isoformat('T')),
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': str(end_time.isoformat('T')),
            'timeZone': 'Europe/Moscow',
        },
    }
    if recurrence:
        event['recurrence'] = [recurrence]
    calendar_id = get_calendar_id(calendar_name)
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



# print()
# create_event('test0', 'qwerty123', 'MSU', 'festival of MSU', datetime.datetime(2019, 4, 12, 8, 30, 0, 0),
#              datetime.datetime(2019, 4, 12, 10, 30, 0, 0), 'RRULE:FREQ=DAILY;COUNT=2')
