from django.db import models
from sessions_coding.models import Classroom_session
# Create your models here.
class Form(models.Model):
    session = models.ForeignKey(Classroom_session, on_delete=models.CASCADE,default=1)
    init_line = models.IntegerField(default=0)
    end_line = models.IntegerField(default=0)
    artificial_name = models.CharField(max_length=30)
    def __str__(self):
        return self.artificial_name

class Form_answer(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    ans_date = models.DateTimeField('date answered',auto_now_add=True, blank=True)
    user = models.EmailField()
    def __str__(self):
        return self.form.artificial_name + '-' + str(ans_date)

class Subject(models.Model):
    subject = models.CharField(max_length=30)
    def __str__(self):
        return self.subject

class Answered_subject(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    ans_form = models.ForeignKey(Form_answer, on_delete=models.CASCADE)
    def __str__(self):
        return self.subject