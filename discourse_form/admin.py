from django.contrib import admin

# Register your models here.
from .models import Form,Form_answer

admin.site.register(Form)
admin.site.register(Form_answer)