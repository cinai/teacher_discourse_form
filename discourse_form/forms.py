from django import forms
from django.db.models import Q
from sessions_coding.models import Classroom_session,Subject,Axis,Skill,Learning_goal,Copus_code

class TeacherDiscourseForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=100,widget=forms.EmailInput(attrs={'class': 'form-control','required':True,'placeholder':'Ingrese aquí su email'}))
    subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.exclude(subject='Ninguna'), widget=forms.CheckboxSelectMultiple())
    copus_code = forms.ModelMultipleChoiceField(queryset=Copus_code.objects.all(),required=False, widget=forms.CheckboxSelectMultiple())#attrs={'class':'list-group'}))
    dummy_copus_code = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        initial_subjects = kwargs.pop('initial_subjects', None)
        initial_email = kwargs.pop('initial_email', None)
        initial_cc = kwargs.pop('initial_cc', None) 
        super().__init__(*args, **kwargs)
        self.fields['subject'].initial = initial_subjects
        self.fields['email'].initial = initial_email
        self.fields['copus_code'].initial = initial_cc

class AfterSubjectForm(forms.Form):
    skill = forms.ModelMultipleChoiceField(queryset=None,required=False, widget=forms.CheckboxSelectMultiple())
    dummy_skill = forms.BooleanField(required=False)
    axis = forms.ModelMultipleChoiceField(queryset=None,required=False, widget=forms.CheckboxSelectMultiple())
    dummy_axis = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        answered_subject = kwargs.pop('subject', None)
        grade_session = kwargs.pop('grade_session', None)
        initial_skills = kwargs.pop('initial_skills', None)
        initial_axis = kwargs.pop('initial_axis', None) 
        super().__init__(*args, **kwargs)
        self.fields['skill'].queryset = Skill.objects.filter(subject=answered_subject.subject)
        self.fields['axis'].queryset = Axis.objects.filter(subject=answered_subject.subject,grade=grade_session)
        self.fields['skill'].initial = initial_skills
        self.fields['axis'].initial = initial_axis

class AfterAxisForm(forms.Form):
    goal = forms.ModelMultipleChoiceField(queryset=None,required=False, widget=forms.CheckboxSelectMultiple())
    dummy_goal = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        answered_axis = kwargs.pop('axis', None)
        initial_goals = kwargs.pop('initial_goals', None)
        super().__init__(*args, **kwargs)
        self.fields['goal'].queryset = Learning_goal.objects.filter(axis=answered_axis.axis)
        self.fields['goal'].initial = initial_goals
