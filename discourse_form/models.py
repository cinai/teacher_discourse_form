from django.db import models
from sessions_coding.models import Classroom_session,Subject,Axis,Skill,Learning_goal,Copus_code

class Discourse_form(models.Model):
    session = models.ForeignKey(Classroom_session, on_delete=models.CASCADE,default=1)
    init_line = models.IntegerField(default=0)
    end_line = models.IntegerField(default=0)
    artificial_name = models.CharField(max_length=30)
    text = models.TextField()
    def __str__(self):
        return self.artificial_name

class Form_answer(models.Model):
    form = models.ForeignKey(Discourse_form, on_delete=models.CASCADE)
    ans_date = models.DateTimeField('date answered',auto_now_add=True, blank=True)
    user = models.EmailField()
    done = models.BooleanField(blank=True,default=False)
    def __str__(self):
        return self.form.artificial_name + '-' + str(self.ans_date)

class Answered_subject(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    ans_form = models.ForeignKey(Form_answer, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.subject)

class Answered_axis(models.Model):
    axis = models.ForeignKey(Axis,on_delete=models.CASCADE)
    ans_form = models.ForeignKey(Form_answer, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.axis)

class Answered_skill(models.Model):
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE)
    ans_form = models.ForeignKey(Form_answer, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.skill)

class Answered_learning_goal(models.Model):
    goal = models.ForeignKey(Learning_goal,on_delete=models.CASCADE)
    ans_form = models.ForeignKey(Form_answer, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.goal)

class Answered_copus_code(models.Model):
    copus_code = models.ForeignKey(Copus_code,on_delete=models.CASCADE)
    ans_form = models.ForeignKey(Form_answer, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.copus_code)

class Answered_axis_phrases(models.Model):
    axis = models.ForeignKey(Answered_axis,on_delete=models.CASCADE)
    ans_form = models.ForeignKey(Form_answer, on_delete=models.CASCADE)
    phrases = models.TextField()
    def __str__(self):
        return str(self.axis)

class Answered_skill_phrases(models.Model):
    skill = models.ForeignKey(Answered_skill,on_delete=models.CASCADE)
    ans_form = models.ForeignKey(Form_answer, on_delete=models.CASCADE)
    phrases = models.TextField()
    def __str__(self):
        return str(self.skill)
