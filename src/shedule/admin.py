from django.contrib import admin
from shedule.models import Shedule, Lesson, Auditory, Teacher

admin.site.register(Shedule)
admin.site.register(Lesson)
admin.site.register(Teacher)
admin.site.register(Auditory)
