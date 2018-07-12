from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
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
    return HttpResponse("Hello, world. You're at the discourse form index.")

def thanks(request):
    return HttpResponse("Gracias por su respuesta")

def get_answers(request,form_id):
    d_form = Discourse_form.objects.get(id=form_id)
    text = d_form.text
    if request.method == 'POST':
        form = TeacherDiscourseForm(request.POST)
        if form.is_valid():
            # save form answer
            email = form.cleaned_data['email']
            ans_form = Form_answer(form=d_form,user=email)
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

           #return get_skills(request,form_id,d_form.id)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherDiscourseForm()

    return render(request, 'formulario.html', {'form': form,'text':text})

def get_skills(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    text = d_form.text
    if request.method == 'POST':
        form_2 = AfterSubjectForm(request.POST)
        if form_2.is_valid():
            d_form = Discourse_form.objects.get(id=form_id)
            mail = signing.loads(user)
            ans_form = Form_answer.objects.get(form=d_form,user=mail)
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

    # if a GET (or any other method) we'll create a blank form
    else:
        form_2 = AfterSubjectForm()

    return render(request, 'formulario2.html', {'form_2': form_2,'text':text})

def get_learning_goals(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    text = d_form.text
    if request.method == 'POST':
        form_3 = AfterAxisForm(request.POST)
        if form_3.is_valid():
            d_form = Discourse_form.objects.get(id=form_id)
            mail = signing.loads(user)
            ans_form = Form_answer.objects.get(form=d_form,user=mail)
            # save goal
            goals = form_3.cleaned_data['goal']
            for goal in goals:
                ans_goal = Answered_learning_goal(ans_form=ans_form,goal=goal)
                ans_goal.save()
            return HttpResponseRedirect(reverse('discourse_form:thanks'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form_3 = AfterAxisForm()

    return render(request, 'formulario3.html', {'form_3': form_3,'text':text})