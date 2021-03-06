import random

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.urls import reverse
from django.core import signing

from .forms import TeacherDiscourseForm,AfterSubjectForm,AfterAxisForm

from .models import (
    Discourse_form,
    Form_answer,
    Answered_subject,
    Answered_axis,
    Answered_skill,
    Answered_learning_goal,
    Answered_copus_code,
    Answered_axis_phrases,
    Answered_skill_phrases,
    Answered_copus_phrases,
    Answered_dialogic_phrases,
    )
from sessions_coding.models import Skill,Learning_goal

CHOICES = [('Autoritativo','Autoritativo'),
            ('Dialogico','Dialógico'),
            ('NA','Ninguna de las anteriores')]

def name_detection(request):
    return render(request, 'html_graph.html')
def name_prop(request):
    return render(request, 'name_proportion.html')

def index(request):
    return render(request, 'login.html')

def thanks(request):
    return render(request, 'gracias.html')

def clean_spaces(a_list):
    new_list = []
    initial = -1
    for i,element in enumerate(a_list):
        if element == "":
            if initial == -1:
                initial = i
        else:
            if initial != -1:
                seconds = (i-initial)*15
                if seconds > 60:
                    if int(seconds/60) > 1:
                        new_list.append('*** Sin transcripción disponible durante '+ str(int(seconds/60)) +' minutos ***')
                    else:
                        new_list.append('*** Sin transcripción disponible durante '+ str(int(seconds/60)) +' minuto ***')
                else:
                    new_list.append('*** Sin transcripción disponible durante '+ str(seconds) +' segundos ***')
                initial = -1
            new_list.append(element)
    return new_list

def get_answers_2(request,form_id):
    d_form = Discourse_form.objects.get(id=form_id)
    text = d_form.text
    form = TeacherDiscourseForm()
    return render(request, 'test2.html', {'form': form,'text':clean_spaces(text.splitlines()),'form_id':form_id})#[x if x!=" " else "-" for x in text.splitlines()]})

def get_answers(request,form_id):
    d_form = Discourse_form.objects.get(id=form_id)
    text = d_form.text
    clean_text = clean_spaces(text.splitlines())
    if request.method == 'POST':
        form = TeacherDiscourseForm(request.POST)
        if form.is_valid():
            # save form answer
            email = form.cleaned_data['email']
            dialogic_list = form.cleaned_data['dialogic']
            ans_form,created = Form_answer.objects.get_or_create(form=d_form,user=email)
            ans_form.dialogic = "-".join(dialogic_list)
            if created:
                ans_form.save()
            else:
                # delete all subjects related to ans_form
                Answered_subject.objects.filter(ans_form=ans_form).delete() 
                # delete all copus code with this stuff
                Answered_copus_code.objects.filter(ans_form=ans_form).delete()
                # delete all copus code with this stuff
                Answered_dialogic_phrases.objects.filter(ans_form=ans_form).delete()
                # 
                ans_form.done = False
                ans_form.save()
            # save subject
            subject = form.cleaned_data['subject']
            subject_NA = False
            for s in subject:
                if str(s) == 'Ninguna de las anteriores':
                    subject_NA =True
                ans_sub = Answered_subject(ans_form=ans_form,subject=s)
                ans_sub.save()
            # save copus codes
            copus_codes = form.cleaned_data['copus_code']
            for code in copus_codes:
                ans_copus = Answered_copus_code(ans_form=ans_form,copus_code=code)
                ans_copus.save()
                cc_phrases_name = 'input_id_copus_code_'+str(ans_copus.copus_code.pk-1)
                for key, value in request.POST.items():
                    if key.startswith(cc_phrases_name):

                        if type(value) == list:
                            for element in value:
                                index_phrases = clean_text.index(element)+1
                                ans_phrases = Answered_copus_phrases(copus=ans_copus,ans_form=ans_form,phrases=element,code=index_phrases)
                                ans_phrases.save()
                        else:
                            index_phrases = clean_text.index(value)+1
                            ans_phrases = Answered_copus_phrases(copus=ans_copus,ans_form=ans_form,phrases=value,code=index_phrases)
                            ans_phrases.save()
            if not 'NA' in dialogic_list:
                for dialogic in dialogic_list:
                    if dialogic.startswith('A'):
                        dialogic_id = 0
                    else:
                        dialogic_id = 1
                    d_phrases_name = 'input_id_dialogic_'+str(dialogic_id)
                    print(d_phrases_name)
                    for key,value in request.POST.items():
                        if key.startswith(d_phrases_name):
                            if type(value) == list:
                                for element in value:
                                    index_phrases = clean_text.index(element)+1
                                    ans_phrases = Answered_dialogic_phrases(dialogic=dialogic,ans_form=ans_form,phrases=element,code=index_phrases)
                                    ans_phrases.save()
                            else:
                                index_phrases = clean_text.index(value)+1
                                ans_phrases = Answered_dialogic_phrases(dialogic=dialogic,ans_form=ans_form,phrases=value,code=index_phrases)
                                ans_phrases.save()
            # redirect to next form
            crypted_mail = signing.dumps(email)
            if subject_NA: # Ningun subject
                ans_form.done = True
                ans_form.save()
                return HttpResponseRedirect(reverse('discourse_form:thanks'))
            return HttpResponseRedirect(reverse('discourse_form:question_2', kwargs={'form_id':form_id,'user':crypted_mail}))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherDiscourseForm()

    return render(request, 'formulario.html', {'form': form,'text':clean_text,'form_id':form_id})#[x if x!=" " else "-" for x in text.splitlines()]})

def get_answers_back(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    text = d_form.text
    mail = signing.loads(user)
    ans_form = Form_answer.objects.get(form=d_form,user=mail)
    subjects = Answered_subject.objects.filter(ans_form=ans_form)
    grade_session = d_form.session.grade
    text = d_form.text
    clean_text = clean_spaces(text.splitlines())
    if request.method == 'POST':
        the_forms = [AfterSubjectForm(request.POST,subject=x,grade_session=grade_session,prefix=x.subject.subject) for x in subjects]
        # if there was a previous answer, delete it
        if Answered_skill.objects.filter(ans_form=ans_form).exists():
            Answered_skill.objects.filter(ans_form=ans_form).delete()
        if Answered_axis.objects.filter(ans_form=ans_form).exists():
            Answered_axis.objects.filter(ans_form=ans_form).delete()
        # save the new answers
        for form_2 in the_forms:
            if form_2.is_valid():
                # save skill
                skills = form_2.cleaned_data['skill']
                for skill in skills:
                    ans_skill = Answered_skill(ans_form=ans_form,skill=skill)
                    ans_skill.save()
                    skill_phrases_name = 'input_id_'+str(ans_skill.skill.subject)+'-skill_'+str(ans_skill.skill.pk)
                    for key, value in request.POST.items():
                        if key.startswith(skill_phrases_name):
                            if type(value) == list:
                                for element in value:
                                    index_phrases = clean_text.index(element)+1
                                    ans_phrases = Answered_skill_phrases(skill=ans_skill,ans_form=ans_form,phrases=element,code=index_phrases)
                                    ans_phrases.save()
                            else:
                                index_phrases = clean_text.index(value)+1
                                ans_phrases = Answered_skill_phrases(skill=ans_skill,ans_form=ans_form,phrases=value,code=index_phrases)
                                ans_phrases.save()
                # save axis1
                axis = form_2.cleaned_data['axis']
                for axe in axis:
                    ans_axe = Answered_axis(ans_form=ans_form,axis=axe)
                    ans_axe.save()

        initial_subjects = [x.subject.id for x in Answered_subject.objects.filter(ans_form=ans_form)]
        initial_cc = [x.copus_code.id for x in Answered_copus_code.objects.filter(ans_form=ans_form)]
        initial_phrases_cc = {}
        for ans_copus in Answered_copus_code.objects.filter(ans_form=ans_form):
            ans_phrases = Answered_copus_phrases.objects.filter(ans_form=ans_form,copus=ans_copus)
            copus_id = ans_copus.copus_code.id
            initial_phrases_cc[copus_id] = []
            if ans_phrases.exists():
                for phrases in ans_phrases:
                    initial_phrases_cc[copus_id].append(phrases.code)
        initial_dialogic = ans_form.dialogic.split('-')
        d_dict = {0:'Autoritativo',1:'Dialogico'}
        list_dialogic = []
        if 'Autoritativo' in initial_dialogic:
            list_dialogic.append(0)
        if 'Dialogico' in initial_dialogic:
            list_dialogic.append(1)
        initial_phrases_d = {}
        for dialogic_id in list_dialogic:
            ans_phrases = Answered_dialogic_phrases.objects.filter(ans_form=ans_form,dialogic=d_dict[dialogic_id])
            if ans_phrases.exists():
                initial_phrases_d[dialogic_id] = []
                for phrases in ans_phrases:
                        initial_phrases_d[dialogic_id].append(phrases.code)
        form = TeacherDiscourseForm(initial_email=mail,initial_subjects=initial_subjects,initial_cc=initial_cc,initial_dialogic=initial_dialogic)
        print(initial_phrases_d)
        return render(request, 'formulario.html', {'form': form,'text':clean_spaces(text.splitlines()),'form_id':form_id,'cc_phrases':initial_phrases_cc,'d_phrases':initial_phrases_d})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def get_skills(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    grade_session = d_form.session.grade
    mail = signing.loads(user)
    ans_form = Form_answer.objects.get(form=d_form,user=mail)
    subjects = Answered_subject.objects.filter(ans_form=ans_form)
    text = d_form.text
    clean_text = clean_spaces(text.splitlines())
    if request.method == 'POST':
        the_forms = [AfterSubjectForm(request.POST,subject=x,grade_session=grade_session,prefix=x.subject.subject) for x in subjects]
        if all([form_2.is_valid() for form_2 in the_forms]):
            # if there was a previous answer, delete it
            if Answered_skill.objects.filter(ans_form=ans_form).exists():
                Answered_skill.objects.filter(ans_form=ans_form).delete()
            if Answered_axis.objects.filter(ans_form=ans_form).exists():
                Answered_axis.objects.filter(ans_form=ans_form).delete()
            # save the new answers
            counter_axis = 0
            for form_2 in the_forms:
                # save skill
                skills = form_2.cleaned_data['skill']
                for skill in skills:
                    ans_skill = Answered_skill(ans_form=ans_form,skill=skill)
                    ans_skill.save()
                    skill_phrases_name = 'input_id_'+str(ans_skill.skill.subject)+'-skill_'+str(ans_skill.skill.pk)
                    for key, value in request.POST.items():
                        if key.startswith(skill_phrases_name):
                            if type(value) == list:
                                for element in value:
                                    index_phrases = clean_text.index(element)+1
                                    ans_phrases = Answered_skill_phrases(skill=ans_skill,ans_form=ans_form,phrases=element,code=index_phrases)
                                    ans_phrases.save()
                            else:
                                index_phrases = clean_text.index(value)+1
                                ans_phrases = Answered_skill_phrases(skill=ans_skill,ans_form=ans_form,phrases=value,code=index_phrases)
                                ans_phrases.save()
                # save axis1
                axis = form_2.cleaned_data['axis']
                for axe in axis:
                    ans_axe = Answered_axis(ans_form=ans_form,axis=axe)
                    ans_axe.save()
                    counter_axis += 1
            # redirect to next form
            if counter_axis > 0:
                return HttpResponseRedirect(reverse('discourse_form:question_3', kwargs={'form_id':form_id,'user':user}))
            else:
                if Answered_learning_goal.objects.filter(ans_form=ans_form).exists():
                    Answered_learning_goal.objects.filter(ans_form=ans_form).delete()
                ans_form.done = True
                ans_form.save()
                return HttpResponseRedirect(reverse('discourse_form:thanks'))
        else:
            print("ERROR")
            context = {}
            context['subjects'] = {}
            for i,ans_subject in enumerate(subjects):
                subject_name = ans_subject.subject.subject
                context['subjects'][subject_name] = the_forms[i]
    else:
        # if a GET (or any other method) we'll create a blank form
        context = {}
        context['subjects'] = {}
        for ans_subject in subjects:
            # send subject name and form
            all_skills = Skill.objects.filter(subject=ans_subject.subject)
            skills_tooltips = {}
            for skill in all_skills:
                d = skill.description
                if d!='nan':
                    skills_tooltips[skill.pk] = d
                else:
                    skills_tooltips[skill.pk] = skill
            subject_name = ans_subject.subject.subject
            # pre_fill
            if Answered_skill.objects.filter(ans_form=ans_form).exists():
                ans_skills =  Answered_skill.objects.filter(ans_form=ans_form)
                initial_skills = [x.skill.id for x in ans_skills]
                initial_phrases_skills = {}
                for skill in ans_skills:
                    ans_phrases = Answered_skill_phrases.objects.filter(ans_form=ans_form,skill=skill)
                    if ans_phrases.exists():
                        skill_id = skill.skill.pk
                        initial_phrases_skills[skill_id] = []
                        for phrases in ans_phrases:
                            initial_phrases_skills[skill_id].append(phrases.code)
            else:
                initial_skills = []
                initial_phrases_skills = {}
            if Answered_axis.objects.filter(ans_form=ans_form).exists():
                initial_axis = [x.axis.id for x in Answered_axis.objects.filter(ans_form=ans_form)]
            else:
                initial_axis = []
            form_2 = AfterSubjectForm(subject=ans_subject,grade_session=grade_session,prefix=subject_name,initial_skills=initial_skills,initial_axis=initial_axis)
            context['subjects'][subject_name] = form_2

    context['skills_tooltips'] = skills_tooltips      
    context['form_phrases'] = initial_phrases_skills
    context['text'] = clean_text
    context['user_m'] = user
    context['form_id'] = form_id
    return render(request, 'formulario2.html', context)

def get_skills_back(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    mail = signing.loads(user)
    ans_form = Form_answer.objects.get(form=d_form,user=mail)
    ans_axis = Answered_axis.objects.filter(ans_form=ans_form)
    if request.method == 'POST':
        the_forms = [AfterAxisForm(request.POST,axis=x,prefix=x.axis.axis) for x in ans_axis]
        if Answered_learning_goal.objects.filter(ans_form=ans_form).exists():
            Answered_learning_goal.objects.filter(ans_form=ans_form).delete()
        for form_3 in the_forms:
            if form_3.is_valid():
                goals = form_3.cleaned_data['goal']
                for goal in goals:
                    ans_goal = Answered_learning_goal(ans_form=ans_form,goal=goal)
                    ans_goal.save()
        return HttpResponseRedirect(reverse('discourse_form:question_2', kwargs={'form_id':form_id,'user':user}))
    return HttpResponseNotFound('<h1>Page not found</h1>')

def get_learning_goals(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    mail = signing.loads(user)
    ans_form = Form_answer.objects.get(form=d_form,user=mail)
    ans_axis = Answered_axis.objects.filter(ans_form=ans_form)
    if request.method == 'POST':
        the_forms = [AfterAxisForm(request.POST,axis=x,prefix=x.axis.axis) for x in ans_axis]
        if all([form_3.is_valid() for form_3 in the_forms]):
            if Answered_learning_goal.objects.filter(ans_form=ans_form).exists():
                Answered_learning_goal.objects.filter(ans_form=ans_form).delete()
            for form_3 in the_forms:
                goals = form_3.cleaned_data['goal']
                for goal in goals:
                    ans_goal = Answered_learning_goal(ans_form=ans_form,goal=goal)
                    ans_goal.save()
            ans_form.done = True
            ans_form.save()
            return HttpResponseRedirect(reverse('discourse_form:thanks'))
        else:
            context = {}
            context['axis'] = {}
            for i,ans_axe in enumerate(ans_axis):
                axe_name = ans_axe.axis.axis
                context['axis'][axe_name] = the_forms[i]
    else:
    # if a GET (or any other method) we'll create a blank form
        context = {}
        context['axis'] = {}
        oa_description = {}
        for ans_axe in ans_axis:
            # send subject name and form
            axe_name = ans_axe.axis.axis
            general_goals = Learning_goal.objects.filter(axis=ans_axe.axis)
            for goal in general_goals:
                d = goal.long_name
                if d!='nan':
                    oa_description[goal.pk] = d
                else:
                    oa_description[goal.pk] = goal
            if Answered_learning_goal.objects.filter(ans_form=ans_form).exists():
                initial_goals = [x.goal.id for x in Answered_learning_goal.objects.filter(ans_form=ans_form)]
            else:
                initial_goals = []
            form_3 = AfterAxisForm(axis=ans_axe,prefix=axe_name,initial_goals=initial_goals)
            context['axis'][axe_name] = form_3 
    text = d_form.text
    context['oa_description'] = oa_description
    context['text'] = clean_spaces(text.splitlines())
    context['user_m'] = user
    context['form_id'] = form_id
    return render(request, 'formulario3.html', context)

def yachao(request):
    return render(request, 'chao.html')

def answers(request,form_id):
    d_form = Discourse_form.objects.get(id=form_id)
    answers = Form_answer.objects.filter(form=d_form)
    context = {}
    context['sesion'] = str(d_form.session.grade)+' - '+d_form.session.content
    context['users_answers'] = []
    for answer in answers:
        a_dict = {}
        a_dict['user'] = answer.user
        a_dict['done'] = answer.done
        a_dict['subject'] = []
        for ans_subject in Answered_subject.objects.filter(ans_form=answer):
            a_dict['subject'].append(ans_subject.subject.subject)
        a_dict['copus_code'] = []
        for ans_copus_code in Answered_copus_code.objects.filter(ans_form=answer):
            a_dict['copus_code'].append(ans_copus_code.copus_code.code)
        a_dict['skill'] = []
        for ans_skill in Answered_skill.objects.filter(ans_form=answer):
            a_dict['skill'].append(ans_skill.skill.skill)
        a_dict['axis'] = []
        for ans_axis in Answered_axis.objects.filter(ans_form=answer):
            a_dict['axis'].append(ans_axis.axis.axis)
        a_dict['oas'] = []
        for ans_oa in Answered_learning_goal.objects.filter(ans_form=answer):
            a_dict['oas'].append(ans_oa.goal.goal_name)
        context['users_answers'].append(a_dict)

    return render(request, 'respuestas.html', context)

import datetime

def forms_to_do(request):
    discourse_forms = Discourse_form.objects.all()
    a_dict = {}
    counter = 0
    for d in discourse_forms:
        try:
            answer = Form_answer.objects.get(form=d.pk,user='pcalfucura@gmail.com')
        except Form_answer.DoesNotExist:
            answer = None
        link = 'https://discurso-docente.herokuapp.com/encuesta/'+str(d.pk)
        if answer:
            a_dict[counter] = {'link':link,'done': answer.done}
        else:
            a_dict[counter] = {'link':link,'done': 0}
        counter += 1

    forms_answered = Form_answer.objects.filter(user='patricio.calfucura@ciae.uchile.cl')
    context = {}
    context['forms_todo'] = a_dict
    return render(request, 'todo.html', context)

def forms_to_do_shuffle(request):
    discourse_forms = Discourse_form.objects.filter(session__teacher=4)
    a_dict = {}
    counter = 0
    counter_shuffle = list(range(len(discourse_forms)))#
    random.shuffle(counter_shuffle)
    for d in discourse_forms:
        c = counter_shuffle[counter]
        d = discourse_forms[c]
        try:
            answer = Form_answer.objects.get(form=d.pk,user='pcalfucura@gmail.com')
        except Form_answer.DoesNotExist:
            answer = None
        link = 'https://discurso-docente.herokuapp.com/encuesta/'+str(d.pk)
        if answer:
            a_dict[counter] = {'link':link,'done': answer.done}
        else:
            a_dict[counter] = {'link':link,'done': 0}
        counter += 1

    #forms_answered = Form_answer.objects.filter(user='patricio.calfucura@ciae.uchile.cl')
    context = {}
    context['forms_todo'] = a_dict
    return render(request, 'todo.html', context)

def forms_to_do_paulina(request):
    discourse_forms = Discourse_form.objects.filter(session__teacher=2)
    a_dict = {}
    counter = 0
    sample = [37, 61, 29, 33, 70, 36, 69, 20, 10, 104, 74, 83, 57, 82, 88, 55, 58, 54, 72, 67, 13, 94, 95, 75, 64, 56, 91, 60, 76, 92]#, 43, 40, 46, 85, 41, 112, 50, 26, 108, 105#], 12, 53, 110, 86, 21, 96, 103, 44, 71, 90]
    for d in discourse_forms:
        if d.pk in sample:
            try:
                answer = Form_answer.objects.get(form=d.pk,user='paulinajaure@gmail.com')
            except Form_answer.DoesNotExist:
                answer = None
            link = 'https://discurso-docente.herokuapp.com/encuesta/'+str(d.pk)
            if answer:
                a_dict[counter] = {'link':link,'done': answer.done}
            else:
                a_dict[counter] = {'link':link,'done': 0}
            counter += 1

    forms_answered = Form_answer.objects.filter(user='paulinajaure@gmail.com')
    context = {}
    context['forms_todo'] = a_dict
    return render(request, 'todo.html', context)

def forms_to_do_cinthia(request):
    discourse_forms = Discourse_form.objects.all()
    a_dict = {}
    counter = 0
    sample = [251, 235, 393, 484, 394, 213, 577, 428, 193, 509, 91, 574, 169, 365, 39, 73, 158, 456, 271, 635, 329, 298, 387, 403, 337, 346, 296, 54, 52, 618, 233, 285, 150, 137, 234, 124, 22, 152, 301, 77, 510, 259, 112, 639, 475, 592, 261, 369, 17, 571, 195, 573, 376, 508, 538, 25, 453, 224, 78, 286]
    for d in discourse_forms:
        if d.pk in sample:
            try:
                answer = Form_answer.objects.get(form=d.pk,user='landeroscastillocj@gmail.com')
            except Form_answer.DoesNotExist:
                answer = None
            link = 'https://discurso-docente.herokuapp.com/encuesta/'+str(d.pk)
            if answer:
                a_dict[counter] = {'link':link,'done': answer.done}
            else:
                a_dict[counter] = {'link':link,'done': 0}
            counter += 1

    forms_answered = Form_answer.objects.filter(user='landeroscastilloc@gmail.com')
    context = {}
    context['forms_todo'] = a_dict
    return render(request, 'todo.html', context)

def forms_to_do_andrea(request):
    discourse_forms = Discourse_form.objects.all()
    a_dict = {}
    counter = 0
    sample = [333, 592, 319, 164, 595, 288, 43, 217, 390, 211, 445, 107, 72, 151, 349, 510, 357, 186, 189, 629, 531, 247, 559, 430, 309, 503, 379, 276, 450, 371, 429, 246, 471, 165, 491, 102, 476, 484, 24, 490, 82, 469, 183, 532, 137, 134, 571, 616, 261, 426, 482, 574, 184, 256, 477, 381, 354, 201, 130, 279]
    for d in discourse_forms:
        if d.pk in sample:
            try:
                answer = Form_answer.objects.get(form=d.pk,user='andmancilla8@gmail.com')
            except Form_answer.DoesNotExist:
                answer = None
            link = 'https://discurso-docente.herokuapp.com/encuesta/'+str(d.pk)
            if answer:
                a_dict[counter] = {'link':link,'done': answer.done}
            else:
                a_dict[counter] = {'link':link,'done': 0}
            counter += 1

    forms_answered = Form_answer.objects.filter(user='andmancilla8@gmail.com')
    context = {}
    context['forms_todo'] = a_dict
    return render(request, 'todo.html', context)