from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/tasks']

def get_credentials():
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_next_weekday_date(weekday_name):
    # Get today's date and weekday index
    today = datetime.date.today()
    weekday_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(weekday_name)

    # Calculate how many days until the target weekday
    days_ahead = weekday_index - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return today + datetime.timedelta(days=days_ahead)

def create_calendar_event(description, datetime_str):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    try:
        parts = datetime_str.split(" at ")
        weekday = parts[0].strip()
        time_str = parts[1].strip()

        event_date = get_next_weekday_date(weekday)
        event_time = datetime.datetime.strptime(time_str, "%I%p").time()
        event_datetime = datetime.datetime.combine(event_date, event_time)

        start_time = event_datetime.isoformat()
        end_time = (event_datetime + datetime.timedelta(hours=1)).isoformat()

        event = {
            'summary': description,
            'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'}
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return created_event.get('htmlLink')

    except Exception as e:
        print(f"⚠️ Error creating event: {e}")
        raise

def create_task(title, due_str=None):
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    task = {'title': title}
    if due_str:
        due_date = datetime.datetime.strptime(due_str, "%A").date()
        now = datetime.date.today()
        due_date = due_date.replace(year=now.year, month=now.month)
        task['due'] = due_date.isoformat() + "T00:00:00.000Z"

    result = service.tasks().insert(tasklist='@default', body=task).execute()
    return result.get('id')
