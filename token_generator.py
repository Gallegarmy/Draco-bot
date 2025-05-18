"""
Used for generating the first token, which is not to be changed.

Preconditions:
    - An app in Google Cloud console must be created
    - The credentials must be created as "Desktop app"
    - The Google Calendar API must be enabled
    - The user owning the calendar (e.g. sysarmygalicia@gmail.com) must authorize the app and share the calendar with it
    - The user (e.g. sysarmygalicia@gmail.com) must be added as "Test user" under "Audience" when in Testing mode

Once you execute this and complete the manual authentication flow only once,
a *.pkl file is remaining as a result. You should use that within the bot for using Calendar API.

"""
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials_desktop.json', SCOPES)

creds = flow.run_local_server(port=0)

# Save token for future use
with open('desktop_token.pkl', 'wb') as token:
    pickle.dump(creds, token)