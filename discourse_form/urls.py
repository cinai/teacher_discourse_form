from django.urls import path

from . import views

app_name = 'discourse_form'

urlpatterns = [
    path('', views.index, name='index'),
    path('encuesta/<int:form_id>/objetivo_de_aprendizaje/<str:user>', views.get_learning_goals, name='question_3'),
    path('encuesta/<int:form_id>/habilidades_y_eje/<str:user>', views.get_skills, name='question_2'),
    path('encuesta/<int:form_id>/', views.get_answers, name='encuesta'),
    path('gracias/', views.thanks, name='thanks'),
]