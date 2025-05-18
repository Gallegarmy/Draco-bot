from googleapiclient.discovery import build
import pickle
import datetime as dt


with open("desktop_token.pkl", "rb") as token:
    creds = pickle.load(token)
service = build("calendar", "v3", credentials=creds)


def create_event(game_info):
    global service

    start_time = dt.time.fromisoformat(game_info['start_time'])
    start_dt = dt.datetime.combine(game_info['start_date'], start_time)

    end_dt = start_dt + dt.timedelta(minutes=120)

    event = {
      'summary': game_info['meeting_name'],
      'location': 'Asociación Draco Rúa Merced, 59, 15009 A Coruña',
      'description': game_info['meeting_description'],
      'start': {
        'dateTime': start_dt.isoformat(),
        'timeZone': 'Europe/Madrid',
      },
      'end': {
        'dateTime': end_dt.isoformat(),
        'timeZone': 'Europe/Madrid',
      },
    }

    calendar_id = "primary"  # or your shared calendar's ID
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event['htmlLink']