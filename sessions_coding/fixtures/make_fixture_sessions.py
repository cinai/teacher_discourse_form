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
counter = 0
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
        a_dict = {'model':'sessions_coding.classroom_session','pk':counter+8,'fields':{'grade':grade,'teacher':teacher,'wav_name':name,'duration':duration,'content':content,'colegio':colegio,'date':date,'path':path}}
        sessions.append((counter+8,filename))
        les_dict.append(a_dict)
        counter += 1

# load 1-20 lines
for s in sessions:
    file_name = os.path.join(sessions_files_path,s[1])
    with open(file_name,'r', encoding="utf8") as f:
        array = []
        c = 0
        for line in f:
            array.append(line)
            c+=1
            if c == 20:
                break
    a_dict = {'model':'discourse_form.discourse_form','pk':s[0],'fields':{'session':s[0],'init_line':1,'end_line':20,'artificial_name':'_'.join([s[1],'1','20']),'text':'\n'.join(array)}}
    les_dict.append(a_dict)
# output the json file
with open('data_sessions_jose.json', 'w') as outfile:
    json.dump(les_dict, outfile)
