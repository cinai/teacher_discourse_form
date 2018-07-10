from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.urls import reverse

from .models import Teacher,Subject,Skill

def index(request):
    latest_teacher_list = Teacher.objects.order_by('-id')[:3]
    context = {
        'latest_teacher_list': latest_teacher_list,
    }
    return render(request,'sessions_coding/index.html',context)

def detail(request, teacher_id):
    teacher = get_object_or_404(Teacher,pk=teacher_id)
    return render(request,'sessions_coding/detail.html',{'teacher':teacher})

def detail_2(request, subject_id):
    subj = get_object_or_404(Subject,pk=subject_id)
    return render(request,'sessions_coding/detail_2.html',{'subject':subj})

def results(request, skill_id):
    skill = get_object_or_404(Skill,pk=skill_id)
    response = "You're looking at the selected skill:  %s."
    return HttpResponse(response % skill.skills)

def vote(request, subject_id):
    subj = get_object_or_404(Subject, pk=subject_id)
    try:
        selected_skill = subj.skill_set.get(pk=request.POST['choice'])
    except (KeyError, Skill.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'sessions_coding/detail_2.html', {
            'subject': subj,
            'error_message': "Aún falta responder campos requeridos.",
        })
    else:
        #selected_skill.votes += 1
        #selected_skill.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('sessions_coding:results', args=(selected_skill.id,)))