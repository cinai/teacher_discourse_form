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
    Answered_copus_code)

def index(request):
    return HttpResponse("Me parece sospechosa tu actitud")

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
    if request.method == 'POST':
        form = TeacherDiscourseForm(request.POST)
        if form.is_valid():
            # save form answer
            email = form.cleaned_data['email']
            ans_form,created = Form_answer.objects.get_or_create(form=d_form,user=email)
            if created:
                ans_form.save()
            else:
                # delete all subjects related to ans_form
                Answered_subject.objects.filter(ans_form=ans_form).delete() 
                # delete all copus code with this stuff
                Answered_copus_code.objects.filter(ans_form=ans_form).delete()
                # 
                ans_form.done = False
                ans_form.save()
            # save subject
            subject = form.cleaned_data['subject']
            for s in subject:
                ans_sub = Answered_subject(ans_form=ans_form,subject=s)
                ans_sub.save()
            # save copus codes
            copus_codes = form.cleaned_data['copus_code']
            for code in copus_codes:
                ans_copus = Answered_copus_code(ans_form=ans_form,copus_code=code)
                ans_copus.save()
            # redirect to next form
            crypted_mail = signing.dumps(email)
            return HttpResponseRedirect(reverse('discourse_form:question_2', kwargs={'form_id':form_id,'user':crypted_mail}))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherDiscourseForm()

    return render(request, 'test.html', {'form': form,'text':text,'form_id':form_id})#[x if x!=" " else "-" for x in text.splitlines()]})

def get_answers(request,form_id):
    d_form = Discourse_form.objects.get(id=form_id)
    text = d_form.text
    if request.method == 'POST':
        form = TeacherDiscourseForm(request.POST)
        if form.is_valid():
            # save form answer
            email = form.cleaned_data['email']
            ans_form,created = Form_answer.objects.get_or_create(form=d_form,user=email)
            if created:
                ans_form.save()
            else:
                # delete all subjects related to ans_form
                Answered_subject.objects.filter(ans_form=ans_form).delete() 
                # delete all copus code with this stuff
                Answered_copus_code.objects.filter(ans_form=ans_form).delete()
                # 
                ans_form.done = False
                ans_form.save()
            # save subject
            subject = form.cleaned_data['subject']
            for s in subject:
                ans_sub = Answered_subject(ans_form=ans_form,subject=s)
                ans_sub.save()
            # save copus codes
            copus_codes = form.cleaned_data['copus_code']
            for code in copus_codes:
                ans_copus = Answered_copus_code(ans_form=ans_form,copus_code=code)
                ans_copus.save()
            # redirect to next form
            crypted_mail = signing.dumps(email)
            return HttpResponseRedirect(reverse('discourse_form:question_2', kwargs={'form_id':form_id,'user':crypted_mail}))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherDiscourseForm()

    return render(request, 'formulario.html', {'form': form,'text':clean_spaces(text.splitlines()),'form_id':form_id})#[x if x!=" " else "-" for x in text.splitlines()]})

def get_answers_back(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    text = d_form.text
    mail = signing.loads(user)
    ans_form = Form_answer.objects.get(form=d_form,user=mail)
    subjects = Answered_subject.objects.filter(ans_form=ans_form)
    grade_session = d_form.session.grade
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
                # save axis
                axis = form_2.cleaned_data['axis']
                for axe in axis:
                    ans_axe = Answered_axis(ans_form=ans_form,axis=axe)
                    ans_axe.save()
        initial_subjects = [x.subject.id for x in Answered_subject.objects.filter(ans_form=ans_form)]
        initial_cc = [x.copus_code.id for x in Answered_copus_code.objects.filter(ans_form=ans_form)]
        form = TeacherDiscourseForm(initial_email=mail,initial_subjects=initial_subjects,initial_cc=initial_cc)
        return render(request, 'formulario.html', {'form': form,'text':clean_spaces(text.splitlines()),'form_id':form_id})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def get_skills(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    grade_session = d_form.session.grade
    mail = signing.loads(user)
    ans_form = Form_answer.objects.get(form=d_form,user=mail)
    subjects = Answered_subject.objects.filter(ans_form=ans_form)
    if request.method == 'POST':
        the_forms = [AfterSubjectForm(request.POST,subject=x,grade_session=grade_session,prefix=x.subject.subject) for x in subjects]
        if all([form_2.is_valid() for form_2 in the_forms]):
            # if there was a previous answer, delete it
            if Answered_skill.objects.filter(ans_form=ans_form).exists():
                Answered_skill.objects.filter(ans_form=ans_form).delete()
            if Answered_axis.objects.filter(ans_form=ans_form).exists():
                Answered_axis.objects.filter(ans_form=ans_form).delete()
            # save the new answers
            for form_2 in the_forms:
                # save skill
                skills = form_2.cleaned_data['skill']
                for skill in skills:
                    ans_skill = Answered_skill(ans_form=ans_form,skill=skill)
                    ans_skill.save()
                # save axis
                axis = form_2.cleaned_data['axis']
                for axe in axis:
                    ans_axe = Answered_axis(ans_form=ans_form,axis=axe)
                    ans_axe.save()
            # redirect to next form
            return HttpResponseRedirect(reverse('discourse_form:question_3', kwargs={'form_id':form_id,'user':user}))
        else:
            print("ERROR")
            context = {}
            context['subjects'] = {}
            #for form_2 in the_forms:
            #    if not form_2.is_valid():
            #        print(form_2.errors)
                # save skill
            for i,ans_subject in enumerate(subjects):
                subject_name = ans_subject.subject.subject
                context['subjects'][subject_name] = the_forms[i]
    else:
        # if a GET (or any other method) we'll create a blank form
        context = {}
        context['subjects'] = {}
        for ans_subject in subjects:
            # send subject name and form
            subject_name = ans_subject.subject.subject
            # pre_fill
            if Answered_skill.objects.filter(ans_form=ans_form).exists():
                initial_skills = [x.skill.id for x in Answered_skill.objects.filter(ans_form=ans_form)]
            else:
                initial_skills = []
            if Answered_axis.objects.filter(ans_form=ans_form).exists():
                initial_axis = [x.axis.id for x in Answered_axis.objects.filter(ans_form=ans_form)]
            else:
                initial_axis = []
            form_2 = AfterSubjectForm(subject=ans_subject,grade_session=grade_session,prefix=subject_name,initial_skills=initial_skills,initial_axis=initial_axis)
            context['subjects'][subject_name] = form_2            
    text = d_form.text
    context['text'] = clean_spaces(text.splitlines())
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
        for ans_axe in ans_axis:
            # send subject name and form
            axe_name = ans_axe.axis.axis
            if Answered_learning_goal.objects.filter(ans_form=ans_form).exists():
                initial_goals = [x.goal.id for x in Answered_learning_goal.objects.filter(ans_form=ans_form)]
            else:
                initial_goals = []
            form_3 = AfterAxisForm(axis=ans_axe,prefix=axe_name,initial_goals=initial_goals)
            context['axis'][axe_name] = form_3 
    text = d_form.text
    context['text'] = clean_spaces(text.splitlines())
    context['user_m'] = user
    context['form_id'] = form_id
    return render(request, 'formulario3.html', context)


def stupid(request):
    return HttpResponseNotFound('<h1>Página no encontrada por la amargura de algunos</h1>')
def yachao(request):
    return render(request, 'chao.html')

def statistics(request,form_id):
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

    return render(request, 'statistics.html', context)