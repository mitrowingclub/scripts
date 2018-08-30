# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/gmail.send']
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials_2.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))


    #majorDimension=COLUMNS&ranges=Daily+schedule!A16%3AH25&valueRenderOption=FORMATTED_VALUE&key={YOUR_API_KEY}
    # Call the Sheets API
    SPREADSHEET_ID = "1DNsXDZshnpqbgEU0hrU0araJIfGHZ-eFij4smZBf05M"
    RANGE_NAME = 'Daily Schedule!A16:H25'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 majorDimension='COLUMNS',
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for col in values:
            print(col)


    message_text = 'hallo'
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    
    message = MIMEText(message_text)
    message['to'] = 'orm@mit.edu'
    message['from'] = 'rimoll@gmail.com'
    message['subject'] = 'sheets'
    ret = {'raw': "".join(map(chr, base64.urlsafe_b64encode(message.as_string().encode('ascii'))))}
    print(message.as_string())
    print(message.as_string().encode('ascii'))
    print(ret)

    try:
        message = (service.users().messages().send(userId='me', body=ret)
                                        .execute())
        print('Message Id: %s' % message['id'])
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
          
    # results = service.users().labels().list(userId='me').execute()
    
    # labels = results.get('labels', [])
    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])

if __name__ == '__main__':
    main()
# [END sheets_quickstart]
