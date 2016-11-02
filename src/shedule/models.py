# coding: utf-8

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from groups.models import FacultyGroup as Group
from library.models import Subject

from dgapservice.settings import STATIC_ROOT
import datetime


class Teacher(models.Model):
	pass


class Auditory(models.Model):
	pass


class Lesson(models.Model):
	group = models.ForeignKey(Group, verbose_name='Группа')
	room = models.ForeignKey(Auditory, verbose_name='Аудитория')
	teacher = models.ForeignKey(Teacher, verbose_name='Преподаватель')
	subject = models.ForeignKey(Subject, verbose_name='Предмет')

	def __str__(self):
		return str(self.group) + ": " + str(self.subject) + " в " + str(self.weekday)

	weekday = models.IntegerField(default=1, verbose_name='День недели', validators=[
		MaxValueValidator(7),
		MinValueValidator(1)
	])




class Shedule(models.Model):
	group = models.ForeignKey(Group, verbose_name='Группа')
	day_of_week = models.IntegerField(default=1, verbose_name='День недели', validators=[
		MaxValueValidator(7),
		MinValueValidator(1)
	])
	lesson_number = models.IntegerField(default=1, verbose_name='Пара', validators=[
		MaxValueValidator(7),
		MinValueValidator(1)
	])
	lesson_title = models.CharField(verbose_name='Предмет', max_length=50, null=True, blank=True)
	teacher = models.CharField(verbose_name='Преподаватель', max_length=50, null=True, blank=True)
	room = models.CharField(verbose_name='Аудитория', max_length=20, null=True, blank=True)

	def __str__(self):
		return str(self.group) + ": day " + str(self.day_of_week) + ", lesson " + str(self.lesson_number) + '.\t' + str(self.lesson_title)

	@staticmethod
	def json_refill():
		import requests

		def get_as_list(url, name):
			try:
				ret = requests.get(url, stream=True).json()[name]
				return ret
			except TypeError:
				return []
			except KeyError:
				return []

		faculties = get_as_list("https://mipt.ru/api/schedule/get_faculties", 'faculties')
		for faculty in faculties:
			if faculty['faculty_name'] == 'ФОПФ':
				print(faculty['faculty_name'])
				groups = get_as_list("https://mipt.ru/api/schedule/get_groups?faculty_id=" + str(faculty['faculty_id']), 'groups')
				for group in groups:
					year = 0
					#year = int(datetime.datetime.today().timetuple()[0])//10 - int(group['group_name'])//10%10
					group_instance, created = Group.objects.get_or_create(group_number=group['group_name'], year=year)
					days = get_as_list("https://mipt.ru/api/schedule/get_schedule?group_id=" + str(group['group_id']), 'days')
					for day in days:
						for i in range(1, len(day['lessons']) + 1):
							Shedule.objects.filter(group=group_instance,
							                       day_of_week=day['weekday'],
							                       lesson_number=i).delete()
							try:
								teacher_name = day['lessons'][i-1]['teachers'][0]["teacher_name"]
							except TypeError:
								teacher_name = ''

							try:
								room = day['lessons'][i-1]['auditories'][0]["auditory_name"]
							except TypeError:
								room = ''

							Shedule.objects.create(group=group_instance,
							                       day_of_week=day['weekday'],
							                       lesson_number=i,
							                       lesson_title=day['lessons'][i-1]['subject'],
							                       teacher=teacher_name,
							                       room=room)

		#   json.dumps(faculties, sort_keys=True, indent=4, ensure_ascii=False)



