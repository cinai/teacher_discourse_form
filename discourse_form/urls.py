from django.urls import path

from . import views

app_name = 'discourse_form'

urlpatterns = [
    path('', views.index, name='index'),
    path('respuestas/<int:form_id>/', views.answers, name='answers'),
    path('test/<int:form_id>/', views.get_answers_2, name='test'),
    path('encuesta/<int:form_id>/', views.get_answers, name='encuesta'),
    path('encuesta/<int:form_id>/objetivo_de_aprendizaje/<str:user>', views.get_learning_goals, name='question_3'),
    path('encuesta/<int:form_id>/habilidades_y_eje/<str:user>/back', views.get_skills_back, name='question_2_back'),
    path('encuesta/<int:form_id>/<str:user>/back', views.get_answers_back, name='encuesta_back'),
    path('encuesta/<int:form_id>/habilidades_y_eje/<str:user>', views.get_skills, name='question_2'),
    path('gracias/', views.thanks, name='thanks'),
    path('encuestas/', views.forms_to_do, name='encuestas'),
    path('yachao/', views.yachao, name='yachao'),
]