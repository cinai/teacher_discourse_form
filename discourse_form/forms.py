from django import forms
from sessions_coding.models import Classroom_session,Subject,Axis,Skill,Learning_goal,Copus_code

class TeacherDiscourseForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=100)
    subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple())
    copus_code = forms.ModelMultipleChoiceField(queryset=Copus_code.objects.all(), widget=forms.CheckboxSelectMultiple())


class AfterSubjectForm(forms.Form):
    skill = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())
    axis = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        pk_subject = kwargs.pop('subject_id', None)
        pk_grade = kwargs.pop('grade_id',None)
        super().__init__(*args, **kwargs)
        self.fields['skill'].queryset = Skill.objects.all()#.filter(subject=pk_subject)
        self.fields['axis'].queryset = Axis.objects.all()#.filter(subject=pk_subject,grade=pk_grade)


class AfterAxisForm(forms.Form):
    goal = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        pk_axis = kwargs.pop('axis_id', None)
        super().__init__(*args, **kwargs)
        self.fields['goal'].queryset = Learning_goal.objects.all()#.filter(axis=pk_axis)
