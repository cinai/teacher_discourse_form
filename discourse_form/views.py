from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from .forms import TeacherDiscourseForm,AfterSubjectForm,AfterAxisForm

def index(request):
    return HttpResponse("Hello, world. You're at the discourse form index.")

def thanks(request):
    return HttpResponse("Gracias por su respuesta")

def get_answers(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TeacherDiscourseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect(reverse('discourse_form:thanks'))
            return HttpResponseRedirect(reverse('discourse_form:question_2'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherDiscourseForm()

    return render(request, 'formulario.html', {'form': form})

def get_skills(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_2 = AfterSubjectForm(request.POST)
        # check whether it's valid:
        if form_2.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('discourse_form:question_3'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form_2 = AfterSubjectForm()

    return render(request, 'formulario2.html', {'form_2': form_2})

def get_learning_goals(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_3 = AfterAxisForm(request.POST)
        # check whether it's valid:
        if form_3.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('discourse_form:thanks'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form_3 = AfterAxisForm()

    return render(request, 'formulario3.html', {'form_3': form_3})