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
    return render(request, 'gracias.html')

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
    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherDiscourseForm()

    return render(request, 'formulario.html', {'form': form,'text':text})#[x if x!=" " else "-" for x in text.splitlines()]})

def get_skills(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    mail = signing.loads(user)
    ans_form = Form_answer.objects.get(form=d_form,user=mail)
    subjects = Answered_subject.objects.filter(ans_form=ans_form)
    if request.method == 'POST':
        the_forms = [AfterSubjectForm(request.POST,subject=x,prefix=x.subject.subject) for x in subjects]
        if all([form_2.is_valid() for form_2 in the_forms]):
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
    # if a GET (or any other method) we'll create a blank form
    context = {}
    context['subjects'] = {}
    for ans_subject in subjects:
        # send subject name and form
        subject_name = ans_subject.subject.subject
        form_2 = AfterSubjectForm(subject=ans_subject,prefix=subject_name)
        context['subjects'][subject_name] = form_2            
    text = d_form.text
    context['text'] = text
    return render(request, 'formulario2.html', context)

def get_learning_goals(request,form_id,user):
    d_form = Discourse_form.objects.get(id=form_id)
    mail = signing.loads(user)
    ans_form = Form_answer.objects.get(form=d_form,user=mail)
    ans_axis = Answered_axis.objects.filter(ans_form=ans_form)
    if request.method == 'POST':
        the_forms = [AfterAxisForm(request.POST,axis=x,prefix=x.axis.axis) for x in ans_axis]
        if all([form_3.is_valid() for form_3 in the_forms]):
            for form_3 in the_forms:
                goals = form_3.cleaned_data['goal']
                for goal in goals:
                    ans_goal = Answered_learning_goal(ans_form=ans_form,goal=goal)
                    ans_goal.save()
            d_form.done = True
            d_form.save()
            return HttpResponseRedirect(reverse('discourse_form:thanks'))
    # if a GET (or any other method) we'll create a blank form
    context = {}
    context['axis'] = {}
    for ans_axe in ans_axis:
        # send subject name and form
        axe_name = ans_axe.axis.axis
        form_3 = AfterAxisForm(axis=ans_axe,prefix=axe_name)
        context['axis'][axe_name] = form_3 
    text = d_form.text
    context['text'] = text
    return render(request, 'formulario3.html', context)