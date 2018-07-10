from django.urls import path

from . import views

app_name = 'discourse_form'

urlpatterns = [
    path('', views.index, name='index'),
    path('encuesta/objetivo_de_aprendizaje', views.get_learning_goals, name='question_3'),
    path('encuesta/habilidades_y_eje', views.get_skills, name='question_2'),
    path('encuesta/', views.get_answers, name='encuesta'),
    path('gracias/', views.thanks, name='thanks'),
]