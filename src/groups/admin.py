from django.contrib import admin
from groups.models import FacultyGroup


class GroupAdmin(admin.ModelAdmin):
	filter_horizontal = ('subjects', )

admin.site.register(FacultyGroup, GroupAdmin)