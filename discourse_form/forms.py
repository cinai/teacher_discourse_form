from django import forms
from sessions_coding.models import Classroom_session,Subject,Axis,Skill,Learning_goal,Copus_code

class TeacherDiscourseForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=100,widget=forms.EmailInput(attrs={'class': 'form-control','required':True,'placeholder':'Ingrese aquí su email'}))
    subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple())
    copus_code = forms.ModelMultipleChoiceField(queryset=Copus_code.objects.all(), widget=forms.CheckboxSelectMultiple())#attrs={'class':'list-group'}))


class AfterSubjectForm(forms.Form):
    skill = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())
    axis = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        answered_subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)
        self.fields['skill'].queryset = Skill.objects.filter(subject=answered_subject.subject)
        self.fields['axis'].queryset = Axis.objects.filter(subject=answered_subject.subject)


class AfterAxisForm(forms.Form):
    goal = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        answered_axis = kwargs.pop('axis', None)
        super().__init__(*args, **kwargs)
        self.fields['goal'].queryset = Learning_goal.objects.filter(axis=answered_axis.axis)
