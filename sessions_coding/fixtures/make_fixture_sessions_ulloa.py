import json
import os
import pandas as pd
import datetime as dt
import numpy as np
# paths
data_path = r"C:\Users\usuario\Documents\Python Scripts\topic_forms\teacher_discourse_form\data"
sessions_path = os.path.join(data_path,'audio_db_simplify.xlsx')
sessions_files_path = os.path.join(data_path,'textos_ulloa')
sessions_filepaths = os.listdir(sessions_files_path)
df_sessions = pd.read_excel(sessions_path)

# aux dict
grades = ['Primero básico','Segundo básico','Tercero básico','Cuarto básico',
'Quinto básico','Sexto básico','Séptimo básico','Octavo básico',
'Primero medio','Segundo medio','Tercero medio','Cuarto medio']
# list that saves the dict models
les_dict = []

sessions = [] # list of paths

max_length = 0
counter = 15
for i,row in df_sessions.iterrows():
    if row.teacher == "Heber":
        folder_name = row.audio_id
        if folder_name in sessions_filepaths:
            if row.grade != row.grade:
                continue
            if row.content != row.content:
                continue
            filename = folder_name+'.txt'
            file_name = os.path.join(sessions_files_path,folder_name,filename)
            try:
                with open(file_name,'r', encoding="utf8") as f:
                    content = f.readlines()
                    if len(content)>max_length:
                        max_length=len(content)
                duration = max_length*15.0/60
            except:
                duration = 0
            teacher = 3
            grade = -1
            for i,element in enumerate(grades):
                if row.grade.startswith(element):
                    grade = i + 1
                    break
            if grade==-1:
                print("WARNING")
                print(row.grade)
            content = row.content
            colegio = 3 # Cordillera
            name = row.file
            path = filename
            try:
                date = str(row.createdAt)#dt.datetime.fromtimestamp(int(row.date)/1000).isoformat()
            except ValueError:
                date = '2018-05-21'
            a_dict = {'model':'sessions_coding.classroom_session','pk':counter,'fields':{'grade':grade,'teacher':teacher,'wav_name':name,'duration':duration,'content':content,'colegio':colegio,'date':date,'path':path}}
            sessions.append((counter,filename))
            les_dict.append(a_dict)
            counter += 1
    else:
        continue
print(len(sessions))
print(counter)
from itertools import islice
import math

for s in sessions:
    file_name = os.path.join(sessions_files_path,s[1][:-4],s[1])
    with open(file_name,'r', encoding="utf8") as f:
        content = f.readlines()
        if len(content)>max_length:
            max_length=len(content)

# list of segments should depend on the maximum of lines (18)
n_segments = math.ceil(max_length/20)
list_of_segments = range(n_segments)
n_todo_sessions = len(sessions) # the ones that are not upload
last_pk = 122
pk2 = last_pk #+ (n_todo_sessions*list_of_segments[0])
for s in sessions:
    file_name = os.path.join(sessions_files_path,s[1][:-4],s[1])
    for i in list_of_segments:
        l_init = 20*i 
        l_end = 20*(i+1)
        with open(file_name,'r', encoding="utf8") as f:
            array = list(islice(f,l_init,l_end))
    # load 1-20 lines
        if len(array) == 0:
            #print("NO more")
            break
        if len(array) < 10:
            #print("INCOMPLETE "+str(file_name))
            break
        else:
            a_dict = {'model':'discourse_form.discourse_form','pk':pk2,'fields':{'session':s[0],'init_line':l_init,'end_line':l_end,'artificial_name':'_'.join([s[1],'1','20']),'text':''.join(array)}}
            les_dict.append(a_dict)
            pk2 += 1

# output the json file
l_init = 20*0 
l_end = 20*(n_segments+1)
with open('data_sessions_heber_'+str(l_init)+'_'+str(l_end)+'.json', 'w') as outfile:
    json.dump(les_dict, outfile)

print(len(sessions))
print(max_length)
print(pk2)
#for s in sessions:
    #file_name = os.path.join(sessions_files_path,s[1])
#    print(s[1])