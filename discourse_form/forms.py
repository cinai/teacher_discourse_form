from django import forms
from django.db.models import Q
from sessions_coding.models import Classroom_session,Subject,Axis,Skill,Learning_goal,Copus_code

class TeacherDiscourseForm(forms.Form):
    CHOICES = [('Autoritativo','Autoritativo'),
            ('Dialogico','Dialógico'),
            ('NA','Ninguna de las anteriores')]
    email = forms.EmailField(label='E-mail', max_length=100,widget=forms.EmailInput(attrs={'class': 'form-control','required':True,'placeholder':'Ingrese aquí su email'}))
    subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.exclude(subject='Ninguna'), widget=forms.CheckboxSelectMultiple())
    copus_code = forms.ModelMultipleChoiceField(queryset=Copus_code.objects.all(),required=False, widget=forms.CheckboxSelectMultiple())#attrs={'class':'list-group'}))
    dummy_copus_code = forms.BooleanField(required=False)
    dialogic = forms.MultipleChoiceField(choices=CHOICES,required=False, widget=forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        initial_subjects = kwargs.pop('initial_subjects', None)
        initial_email = kwargs.pop('initial_email', None)
        initial_cc = kwargs.pop('initial_cc', None) 
        initial_dialogic = kwargs.pop('initial_dialogic', None)
        super().__init__(*args, **kwargs)
        self.fields['subject'].initial = initial_subjects
        self.fields['email'].initial = initial_email
        self.fields['copus_code'].initial = initial_cc
        self.fields['dialogic'].initial = initial_dialogic

    def is_valid(self):
        valid = super(TeacherDiscourseForm, self).is_valid()
        if not valid:
            return valid
        copus_codes = self.cleaned_data['copus_code']
        if len(copus_codes) == 0:
            dummy_cc = self.cleaned_data['dummy_copus_code']
            return dummy_cc
        return True
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
        #if initial_skills == []:
         #   self.fields['dummy_skill'].initial = True
       # if initial_axis == []:
         #   self.fields['dummy_axis'].initial = True
    def is_valid(self):
        valid = super(AfterSubjectForm, self).is_valid()
        if not valid:
            return valid
        #skills = self.cleaned_data['skill']
       # if len(skills) == 0:
        #    dummy_s = self.cleaned_data['dummy_skill']
        #    if dummy_s == False:
        #        return False
        #axis = self.cleaned_data['axis']
        #if len(axis) == 0:
        #    dummy_a = self.cleaned_data['dummy_axis']
        #    return dummy_a
        return True

class AfterAxisForm(forms.Form):
    goal = forms.ModelMultipleChoiceField(queryset=None,required=False, widget=forms.CheckboxSelectMultiple())
    dummy_goal = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        answered_axis = kwargs.pop('axis', None)
        initial_goals = kwargs.pop('initial_goals', None)
        super().__init__(*args, **kwargs)
        self.fields['goal'].queryset = Learning_goal.objects.filter(axis=answered_axis.axis)
        self.fields['goal'].initial = initial_goals

    def is_valid(self):
        valid = super(AfterAxisForm, self).is_valid()
        if not valid:
            return valid
        #goals = self.cleaned_data['goal']
        #if len(goals) == 0:
        #    dummy_g = self.cleaned_data['dummy_goal']
        #    return dummy_g
        return True

class selectLines(forms.Form):
    phrases = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        load_phrases = kwargs.pop('load_phrases', None)
        super().__init__(*args, **kwargs)
        self.fields['phrases'].choices = load_phrases
