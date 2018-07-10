from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(School)
admin.site.register(Grade)
admin.site.register(Teacher)
admin.site.register(Classroom_session)
admin.site.register(Subject)
admin.site.register(Axis)
admin.site.register(Learning_goal)
admin.site.register(Skill)
admin.site.register(Copus_code)



