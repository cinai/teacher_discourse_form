from django.contrib import admin

# Register your models here.
from .models import (
	Discourse_form,
	Form_answer,
	Answered_subject,
	Answered_skill,
	Answered_axis,
	Answered_learning_goal,
	Answered_copus_code,
	Answered_axis_phrases,
	Answered_skill_phrases,
	Answered_copus_phrases,
	Answered_dialogic_phrases,

	)

admin.site.register(Discourse_form)
admin.site.register(Form_answer)
admin.site.register(Answered_subject)
admin.site.register(Answered_skill)
admin.site.register(Answered_axis)
admin.site.register(Answered_learning_goal)
admin.site.register(Answered_copus_code)
admin.site.register(Answered_axis_phrases)
admin.site.register(Answered_skill_phrases)
admin.site.register(Answered_copus_phrases)
admin.site.register(Answered_dialogic_phrases)

