import json
import os
import pandas as pd

# paths
data_path = r"C:\Users\usuario\Documents\Python Scripts\topic_forms\teacher_discourse_form\data"
subject_path = os.path.join(data_path,'asignaturas.xlsx')
skills_path = os.path.join(data_path,'habilidades.xlsx')
oa_path = os.path.join(data_path,'listado_oas.xls')
# load excels
df_subjects = pd.read_excel(subject_path)
df_skills = pd.read_excel(skills_path)
df_oa = pd.read_excel(oa_path)

# list that saves the dict models
les_dict = []

# load teacher
teachers = ['Patricio Calfucura','José Gonzáles','Heber Ulloa']

for pk,teacher in enumerate(teachers):
	a_dict = {'model':'sessions_coding.teacher','pk':pk+1,'fields':{'teacher':teacher}}
	les_dict.append(a_dict)

# load schools
schools = ['Cordillera','Santa Rita','Grace Collage']

for pk,school in enumerate(schools):
	a_dict = {'model':'sessions_coding.school','pk':pk+1,'fields':{'school':school}}
	les_dict.append(a_dict)

# load subjects
subjects = ['Matemáticas','Ciencias Naturales','Lenguaje',
'Historia, Geografía y Ciencias Sociales']

for pk,subject in enumerate(subjects):
	a_dict = {'model':'sessions_coding.subject','pk':pk+1,'fields':{'subject':subject}}
	les_dict.append(a_dict)

# load grades
grades = ['Primero básico','Segundo básico','Tercero básico','Cuarto básico',
'Quinto básico','Sexto básico','Séptimo básico','Octavo básico',
'Primero medio','Segundo medio','Tercero medio','Cuarto medio']

for pk,grade in enumerate(grades):
	a_dict = {'model':'sessions_coding.grade','pk':pk+1,'fields':{'grade':grade}}
	les_dict.append(a_dict)

# load copus codes #check the output then
copus_codes = [{"model": "sessions_coding.copus_code", "pk": 1, "fields": {"code": "Expo", "long_name": "Exponiendo, presentando contenido, derivando resultados matem\u00e1ticos, presentando la soluci\u00f3n a un problema, etc.", "eng_code": "Lec"}}, {"model": "sessions_coding.copus_code", "pk": 2, "fields": {"code": "Espera", "long_name": "Esperando, en un momento en que est\u00e1 la posibilidad de interactuar o observar alguna actividad y el profesor no lo est\u00e1 haciendo", "eng_code": "W"}}, {"model": "sessions_coding.copus_code", "pk": 3, "fields": {"code": "Pizarr", "long_name": "Escribiendo en la pizarra (suele marcarse junto a Exponiendo)", "eng_code": "RtW"}}, {"model": "sessions_coding.copus_code", "pk": 4, "fields": {"code": "Retro", "long_name": "Dando retroalimentaci\u00f3n o seguimiento sobre una pregunta o actividad a la clase completa", "eng_code": "FUp"}}, {"model": "sessions_coding.copus_code", "pk": 5, "fields": {"code": "Preg", "long_name": "Preguntando a los estudiantes", "eng_code": "PQ"}}, {"model": "sessions_coding.copus_code", "pk": 6, "fields": {"code": "Escu", "long_name": "Escuchando o respondiendo una pregunta de un estudiante, con el resto de la clase escuchando", "eng_code": "AnQ"}}, {"model": "sessions_coding.copus_code", "pk": 7, "fields": {"code": "Mov", "long_name": "Movi\u00e9ndose a trav\u00e9s de la sala guiando el trabajo de estudiantes durante tareas de aprendizaje activo", "eng_code": "MG"}}, {"model": "sessions_coding.copus_code", "pk": 8, "fields": {"code": "1a1", "long_name": "Discusi\u00f3n extendida uno a uno, entre el profesor y uno o pocos estudiantes, sin prestar atenci\u00f3n al resto de la clase. Usualmente marcada junto a [Mov] o [Escu].", "eng_code": "1o1"}}, {"model": "sessions_coding.copus_code", "pk": 9, "fields": {"code": "Mos", "long_name": "Mostrando o llevando a cabo un experimento, v\u00eddeo, animaci\u00f3n, demostraci\u00f3n o simulaci\u00f3n.", "eng_code": "D/V"}}, {"model": "sessions_coding.copus_code", "pk": 10, "fields": {"code": "Admin", "long_name": "Administrando la sala (asignar tareas, recibir pruebas, etc.)", "eng_code": "Adm"}}]
les_dict = les_dict + copus_codes

# load skills
dict_subject_id = {}
dict_subject = {}
for i,row in df_subjects.iterrows():
	dict_subject_id[row.subsector_id] = row.pk
	dict_subject[row.nombre] = row.pk


for i,row in df_skills.iterrows():
	description = row.descripcion
	if description != description:
		description = ""
	a_dict = {'model':'sessions_coding.skill','pk':row.id,'fields':{'skill':row.nombre,'subject':dict_subject_id[row.subsector_id],'description':row.descripcion}}
	les_dict.append(a_dict)

# load axis and oa
dict_axis = {}
counter = 1
for i,row in df_oa.iterrows():
	super_key = row.subsector+str(row.nivel)+row.eje
	if not super_key in dict_axis:
		# add axis
		dict_axis[super_key] = counter
		a_dict = {'model':'sessions_coding.axis','pk':counter,'fields':{'axis':row.eje,'subject':dict_subject[row.subsector],'grade':row.nivel}}
		les_dict.append(a_dict)
		counter += 1
	# add oa
	desccorta = row.desccorta
	if desccorta != desccorta:
		desccorta = row.desclarga
	a_dict = {'model':'sessions_coding.learning_goal','pk':row.id,'fields':{'goal_name':desccorta,'long_name':row.desclarga,'axis':dict_axis[super_key]}}
	les_dict.append(a_dict)

# output the json file
with open('fixtures\data_try.json', 'w') as outfile:
	json.dump(les_dict, outfile)

