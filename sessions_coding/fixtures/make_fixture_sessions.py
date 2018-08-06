import json
import os
import pandas as pd
import datetime as dt
import numpy as np
# paths
data_path = r"C:\Users\usuario\Documents\Python Scripts\topic_forms\teacher_discourse_form\data"
sessions_path = os.path.join(data_path,'audios_jose.xlsx')
sessions_files_path = os.path.join(data_path,'textos_jose')
sessions_filepaths = os.listdir(sessions_files_path)
df_sessions = pd.read_excel(sessions_path)
# list that saves the dict models
les_dict = []

sessions = [] # list of paths

counter = 8
for i,row in df_sessions.iterrows():
    filename = row.file[:-4] + '.txt'
    if row.resumen=='Valido' and filename in sessions_filepaths:
        if row.grade != row.grade:
            continue
        if row.content != row.content:
            continue
        if row.minutos == row.minutos:
            duration = row.minutos
        else:
            duration = 0
        teacher = 2
        grade = row.grade
        content = row.content
        colegio = 1 # Cordillera
        name = row.file
        path = filename
        try:
            date = dt.datetime.fromtimestamp(int(row.date)/1000).isoformat()
        except ValueError:
            date = '2018-05-21'
        #a_dict = {'model':'sessions_coding.classroom_session','pk':counter,'fields':{'grade':grade,'teacher':teacher,'wav_name':name,'duration':duration,'content':content,'colegio':colegio,'date':date,'path':path}}
        sessions.append((counter,filename))
        #les_dict.append(a_dict)
        counter += 1

from itertools import islice

#i = 5
for i in [6,7,8,9,10,11,12,13,14]:
    pk2 = 8 + (7*i)
    l_init = 20*i + 1
    l_end = 20*(i+1) + 1
    # load 1-20 lines
    for s in sessions:
        file_name = os.path.join(sessions_files_path,s[1])
        with open(file_name,'r', encoding="utf8") as f:
            array = list(islice(f,l_init,l_end))
        a_dict = {'model':'discourse_form.discourse_form','pk':pk2,'fields':{'session':s[0],'init_line':l_init,'end_line':l_end,'artificial_name':'_'.join([s[1],'1','20']),'text':''.join(array)}}
        les_dict.append(a_dict)
        pk2 += 1
    # output the json file
l_init = 20*6 + 1
l_end = 20*(14+1) + 1

with open('data_sessions_jose_'+str(l_init)+'_'+str(l_end)+'.json', 'w') as outfile:
    json.dump(les_dict, outfile)
