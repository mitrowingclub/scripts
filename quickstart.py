# Copyright 2018 MITRC ;)
# MIT license

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import base64
import pandas as pd

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors
from bs4 import BeautifulSoup

test_mode = True

def process_values(values):
    df = pd.DataFrame(values).transpose()
    df = df.drop(1,axis=1) #spurious axis
    
    df = df.applymap(lambda x: None if x == 'empty' else x) # handle empty
    df = df[df.columns[~df.isna().apply(all,axis=0)]] ## filter fully empty columns
    df = df.reset_index(drop=True)
    return df

def render_table(df):
    # make it look prettier:
    df.loc[0:1,2] = df.loc[0:1,0] # pet peeve: show coach cox above number.
    df.loc[0:1,0] = ''
    df = df.fillna('')
    
    table_styles = [dict(selector='', props=[('margin', 0), ('font-family', 'monospace')]),
             dict(selector='.row0', props=[('background-color', '#aaa')]),
            dict(selector='.row1', props=[('background-color', '#ccc')]),
            dict(selector='.col1', props=[('background-color', '#ccc')]),
                    dict(selector='tr:hover', props=[('background-color', '#ffff99')]),
               ]
    obj = df.style.set_table_styles(table_styles).hide_index()
    rend = obj.render(head='')
    
    soup = BeautifulSoup(rend, 'html.parser')
    stl = soup.find_all('style')[0]
    tab = soup.find_all('table')[0]
    
    return stl.__repr__(),tab.__repr__()


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/gmail.send']

# If using new spreadsheet, update these two.
SPREADSHEET_ID = '1aLL8X_e5uLGVcoVuqmxuQVMLBR1cvphnX3Qar1lG9T4'
SPREADSHEET_LINK= 'https://docs.google.com/spreadsheets/d/{sid}/edit#gid=1189084842'.format(sid=SPREADSHEET_ID)


def get_cell_range(ts):
    ''' use the timestamp for the day you want, not for the email day'''
    
    K_LENGTH = 10
    K_START = 6

    start = K_START + ts.dayofweek*K_LENGTH ## eg. Monday => dayofweek=0 => answer=A6:H15
    end = start + K_LENGTH - 1
    return 'A{start}:H{end}'.format(start=start, end=end)


def main():
    curr_ts = pd.Timestamp.today(tz='EST')
    row_ts = curr_ts + pd.to_timedelta('1 day')
    if row_ts.dayofweek not in range(0,5):
        print('no need to send reminder right now: ', curr_ts)
        return 0
    
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials_2.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))


    cell_range= get_cell_range(row_ts)
    range_name = 'Daily schedule!{cell_range}'.format(cell_range=cell_range)
    
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 majorDimension='COLUMNS',
                                                 range=range_name).execute()
    values = result.get('values', [])
    print(values)

    if not values:
        print('No data found.')

    df = process_values(values) 
    stl,tab = render_table(df)
    
    template = """
<html>
<head>
{style}
</head>
<body>
{test_disclaimer}<br/>
Hi rowers,<br/><br/>
 
Here is the schedule for tomorrow. Everyone listed below should be downstairs in the boathouse by 5:55 am, ready to be on the water at 6. Note that coaches will set the lineup in the morning, and may switch people between boats.
<br/>
<br/>
Happy rowing and GO TECH!<br/>
-Your friendly rowing bot.<br/>
<br/>
{table}
<br/>
<br/>

This week's schedule in full is here:<br/>
{sheet_url}<br/><br/>

P.S Issues with this email? In that case, reply-all.<br/>

</body>
</html>
"""
    sheet_url = '{base_link}&range={cell_range}'.format(base_link=SPREADSHEET_LINK, cell_range=cell_range)
    message_text = template.format(sheet_url=sheet_url, table=tab, style=stl, test_disclaimer='(this email is a test, pls ignore)' if test_mode else '')
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    message = MIMEText(message_text, _subtype='html')

    to_list = ['orm@mit.edu'] if test_mode else  ['mitrc-active@mit.edu']
    message['to'] = ','.join(to_list)
    message['cc'] = ','.join(['mitrc.schedule@gmail.com'])
    message['from'] = 'rowing-bot'

    friendly_date = '{day_name} {month_name} {day_number}'.format(day_name=row_ts.day_name(), month_name=row_ts.month_name(), day_number = row_ts.day)
    message['subject'] = 'Rowing reminder for {friendly_date}{test_mode}'.format(friendly_date=friendly_date, test_mode='(Test email)' if test_mode else '')
    ret = {'raw': "".join(map(chr, base64.urlsafe_b64encode(message.as_string().encode())))}

    try:
        message = (service.users().messages().send(userId='me', body=ret)
                                        .execute())
        print('Message Id: %s' % message['id'])
    except errors.HttpError as error:
        print('An error occurred: %s' % error)          

if __name__ == '__main__':
    main()
