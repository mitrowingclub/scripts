
# coding: utf-8

# In[178]:


import pandas as pd
from bs4 import BeautifulSoup
import bs4


# In[179]:


values = [['coach', 'cox', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday'], ['2', '2', '2', '2', '2', '2', '2', '2', '2', '2'], ['*', '', '1', '2', '3', '4', '5', '6', '7', '8'], ['John Cotter', 'Jayanth Uppaluri', 'Anita Chandrahas', 'Joleen Heiderich', 'Mary Kate Manhard', 'Jim Serdy ', 'Kevin Sitek', 'Gowtham Thakku', 'Ruizhi (Ray) Liao', 'Christine Kerney-Slocombe'], ['Andre Bastos', 'Andrew Cunningham', 'Audrey Bazerghi', 'Shijie Gu', 'Richard McWalter', 'Will Suter', 'Yongjin Park', 'Arno Schneuwly', 'Luzi Sennhauser', 'Sarah Trice'], ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'], ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'], ['Glenn Beauchemin', 'Ryan Bellmore', 'Yang Dai', 'Juan Pablo Duarte Pardo', 'Marco Lucente', 'Leandro Araujo', 'Elisa Carmo', 'Nick Yerin', 'Leonardo Aguiar', 'Marien Kamal']]


# In[180]:


def process_values(values):
    df = pd.DataFrame(values).transpose()
    df = df.drop(1,axis=1).applymap(lambda x: None if x == 'empty' else x).dropna(axis=1)
    return df

def render_table(df):
    table_styles = [dict(selector='', props=[('margin', 0), ('font-family', 'monospace')]),
             dict(selector='.row0', props=[('background-color', '#aaa')]),
            dict(selector='.row1', props=[('background-color', '#ccc')]),
            dict(selector='tr:hover', props=[('background-color', '#ffff99')]),
               ]
    obj = df.style.set_table_styles(table_styles).hide_index()
    rend = obj.render(head='')
    
    soup = BeautifulSoup(rend, 'html.parser')
    stl = soup.find_all('style')[0]
    tab = soup.find_all('table')[0]
    
    return stl,tab


# In[181]:


df = process_values(values)
stl,tab = render_table(df)


# In[183]:


stl

