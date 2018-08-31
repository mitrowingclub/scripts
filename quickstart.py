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
import pandas as pd

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors
def process_values(values):
    df = pd.DataFrame(values).transpose()
    df = df.drop(1,axis=1).applymap(lambda x: None if x == 'empty' else x).dropna(axis=1)
    return df

def render_table(df):
    table_styles = [dict(selector='', props=[('margin', 0), ('font-family', 'monospace')]),
                    dict(selector='.row0', props=[('background-color', '#aaa')]),
                    dict(selector='.row1', props=[('background-color', '#ccc')]),
                    dict(selector='tr:hover', props=[('background-color', '#ffff99')])
    ]

    obj = df.style.set_table_styles(table_styles).hide_index()
    rend = obj.render(head='')
    return rend

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/gmail.send']
def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials_2.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    SPREADSHEET_ID = "1DNsXDZshnpqbgEU0hrU0araJIfGHZ-eFij4smZBf05M"
    RANGE_NAME = 'Daily Schedule!A16:H25'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 majorDimension='COLUMNS',
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    print(values)

    if not values:
        print('No data found.')

    df = process_values(values) #pd.DataFrame(values[1:]).transpose()
    fmt_msg = render_table(df)
    
    template = """
<html>
<head>
{style}
</head>
<body>
Hi everyone,<br/><br/>
 
Here is the schedule for tomorrow {weekday} {date}.<br/><br/>

Everyone listed below should be downstairs in the boathouse by 5:55 am, ready to be on the water at 6 am.  Please note that this is not a lineup.  The coaches will set the lineup in the morning, and may switch people between boats.
<br/>
<br/>
Happy rowing and GO TECH!<br/>
-Your friendly reminder bot.<br/>
<br/>
{table}
<br/>
<br/>
P.S. The full week's schedule can be found here:<br/>
{sheet_url}<br/><br/>

</body>
</html>
"""

    stl = '<style type="text/css">\n    #T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9  {\n          margin: 0;\n          font-family: monospace;\n    }    #T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9 .row0 {\n          background-color: #aaa;\n    }    #T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9 .row1 {\n          background-color: #ccc;\n    }    #T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9 tr:hover {\n          background-color: #ffff99;\n    }</style>'

    tab = '<table id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9">\n<thead> <tr>\n<th class="col_heading level0 col0">0</th>\n<th class="col_heading level0 col1">2</th>\n<th class="col_heading level0 col2">3</th>\n<th class="col_heading level0 col3">4</th>\n<th class="col_heading level0 col4">7</th>\n</tr></thead>\n<tbody> <tr>\n<td class="data row0 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row0_col0">coach</td>\n<td class="data row0 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row0_col1">*</td>\n<td class="data row0 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row0_col2">John Cotter</td>\n<td class="data row0 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row0_col3">Andre Bastos</td>\n<td class="data row0 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row0_col4">Glenn Beauchemin</td>\n</tr> <tr>\n<td class="data row1 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row1_col0">cox</td>\n<td class="data row1 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row1_col1"></td>\n<td class="data row1 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row1_col2">Jayanth Uppaluri</td>\n<td class="data row1 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row1_col3">Andrew Cunningham</td>\n<td class="data row1 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row1_col4">Ryan Bellmore</td>\n</tr> <tr>\n<td class="data row2 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row2_col0">Tuesday</td>\n<td class="data row2 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row2_col1">1</td>\n<td class="data row2 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row2_col2">Anita Chandrahas</td>\n<td class="data row2 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row2_col3">Audrey Bazerghi</td>\n<td class="data row2 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row2_col4">Yang Dai</td>\n</tr> <tr>\n<td class="data row3 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row3_col0">Tuesday</td>\n<td class="data row3 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row3_col1">2</td>\n<td class="data row3 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row3_col2">Joleen Heiderich</td>\n<td class="data row3 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row3_col3">Shijie Gu</td>\n<td class="data row3 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row3_col4">Juan Pablo Duarte Pardo</td>\n</tr> <tr>\n<td class="data row4 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row4_col0">Tuesday</td>\n<td class="data row4 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row4_col1">3</td>\n<td class="data row4 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row4_col2">Mary Kate Manhard</td>\n<td class="data row4 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row4_col3">Richard McWalter</td>\n<td class="data row4 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row4_col4">Marco Lucente</td>\n</tr> <tr>\n<td class="data row5 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row5_col0">Tuesday</td>\n<td class="data row5 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row5_col1">4</td>\n<td class="data row5 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row5_col2">Jim Serdy </td>\n<td class="data row5 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row5_col3">Will Suter</td>\n<td class="data row5 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row5_col4">Leandro Araujo</td>\n</tr> <tr>\n<td class="data row6 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row6_col0">Tuesday</td>\n<td class="data row6 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row6_col1">5</td>\n<td class="data row6 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row6_col2">Kevin Sitek</td>\n<td class="data row6 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row6_col3">Yongjin Park</td>\n<td class="data row6 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row6_col4">Elisa Carmo</td>\n</tr> <tr>\n<td class="data row7 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row7_col0">Tuesday</td>\n<td class="data row7 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row7_col1">6</td>\n<td class="data row7 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row7_col2">Gowtham Thakku</td>\n<td class="data row7 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row7_col3">Arno Schneuwly</td>\n<td class="data row7 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row7_col4">Nick Yerin</td>\n</tr> <tr>\n<td class="data row8 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row8_col0">Tuesday</td>\n<td class="data row8 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row8_col1">7</td>\n<td class="data row8 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row8_col2">Ruizhi (Ray) Liao</td>\n<td class="data row8 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row8_col3">Luzi Sennhauser</td>\n<td class="data row8 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row8_col4">Leonardo Aguiar</td>\n</tr> <tr>\n<td class="data row9 col0" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row9_col0">Tuesday</td>\n<td class="data row9 col1" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row9_col1">8</td>\n<td class="data row9 col2" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row9_col2">Christine Kerney-Slocombe</td>\n<td class="data row9 col3" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row9_col3">Sarah Trice</td>\n<td class="data row9 col4" id="T_dd819d8c_ad66_11e8_8ed9_3497f65a40f9row9_col4">Marien Kamal</td>\n</tr></tbody>\n</table>'
    message_text = template.format(weekday='Thursday', date='09/09', sheet_url='www.foo.com', table=tab, style=stl)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    message = MIMEText(message_text, _subtype='html')
    message['to'] = 'orm@mit.edu'
    message['from'] = 'reminder-bot'
    message['subject'] = 'MITRC reminder email'
    ret = {'raw': "".join(map(chr, base64.urlsafe_b64encode(message.as_string().encode())))}

    try:
        message = (service.users().messages().send(userId='me', body=ret)
                                        .execute())
        print('Message Id: %s' % message['id'])
    except errors.HttpError as error:
        print('An error occurred: %s' % error)          

if __name__ == '__main__':
    main()
