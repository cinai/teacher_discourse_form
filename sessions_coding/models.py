from django.db import models
from django.conf import settings

class Grade(models.Model):
	grade = models.CharField(max_length=30)
	def __str__(self):
		return self.grade

class Teacher(models.Model):
	teacher = models.CharField(max_length=30)
	def __str__(self):
		return self.teacher

class School(models.Model):
	school = models.CharField(max_length=30)
	def __str__(self):
		return self.school

class Classroom_session(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    wav_name = models.CharField(max_length=30)
    duration = models.IntegerField(default=0,blank=True)
    content = models.CharField(max_length=30,blank=True)
    colegio = models.ForeignKey(School,on_delete=models.CASCADE,blank=True)
    date = models.DateTimeField(blank=True,null=True)
    path = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY,max_length=300)
    def __str__(self):
        return self.content

class Subject(models.Model):
    subject = models.CharField(max_length=40)
    def __str__(self):
        return self.subject

class Axis(models.Model):
    axis = models.CharField(max_length=30)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.axis

class Skill(models.Model):
    skill = models.CharField(max_length=40)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    def __str__(self):
        return self.skill

class Learning_goal(models.Model):
    goal_name = models.CharField(max_length=100)
    long_name = models.TextField()
    axis = models.ForeignKey(Axis,on_delete=models.CASCADE)
    def __str__(self):
        return self.goal_name

class Copus_code(models.Model):
    code = models.CharField(max_length=4)
    long_name = models.TextField()
    eng_code = models.CharField(max_length=4)
    def __str__(self):
        return self.code
