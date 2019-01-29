import json
import os
import pandas as pd
import sys
# paths
data_path = r"C:\Users\usuario\Documents\Python Scripts\topic_forms\teacher_discourse_form\data"
subject_path = os.path.join(data_path,'asignaturas.xlsx')
skills_path = os.path.join(data_path,'habilidades.xlsx')
oa_path = os.path.join(data_path,'listado_oas.xls')
# load excels
df_oa = pd.read_excel(oa_path,encoding='utf-8)')


# load axis and oa
dict_axis = {}
counter = 1
for i,row in df_oa.iterrows():
	desccorta = row.desccorta
	if desccorta != desccorta:
		df_oa.loc[i,'desccorta'] = str(row.desclarga)

# output the json file
#with open('fixtures\data_try.json', 'w') as outfile:
#	json.dump(les_dict, outfile)
df_oa.to_excel('list_oas_shortdescription.xlsx')
#df_oa.to_csv('list_oas_shortdescription.csv')

