# coding: utf-8

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from groups.models import FacultyGroup as Group
from library.models import Subject

from dgapservice.settings import STATIC_ROOT
import datetime

rings = {
	0: 'Неизвестно',
	1: '9:00 - 10:25',
	2: '10:45 - 12:10',
	3: '12:20 - 13:45',
	4: '13:55 - 15:20',
	5: '15:30 - 16:55',
	6: '17:05 - 18:30',
	7: '18:30 - 19:50',
}

weekdays = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница', 6: 'Суббота'}


class Teacher(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return str(self.name)

	def get_link(self):
		return 'http://wikimipt.org/wiki/' + '_'.join(str(self.name).split(' '))


class Auditory(models.Model):
	name = models.CharField(max_length=25)

	def __str__(self):
		return str(self.name)


class Lesson(models.Model):
	group = models.ForeignKey(Group, verbose_name='Группа')
	room = models.ForeignKey(Auditory, verbose_name='Аудитория', blank=True, null=True)
	teacher = models.ForeignKey(Teacher, verbose_name='Преподаватель', blank=True, null=True)
	subject = models.ForeignKey(Subject, verbose_name='Предмет', blank=True, null=True)

	def __str__(self):
		return str(self.group) + ": " + str(self.subject) + " в " + str(self.weekday)

	weekday = models.IntegerField(default=datetime.datetime.today().weekday(), verbose_name='День недели', choices=weekdays.items())
	time_interval = models.IntegerField(choices=rings.items(), blank=False, default=0)

	@staticmethod
	def json_refill():

		def get_as_list(url, name):
			import requests
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
				groups = get_as_list("https://mipt.ru/api/schedule/get_groups?faculty_id=" + str(faculty['faculty_id']), 'groups')
				for group in groups:
					year = int(datetime.datetime.today().timetuple()[0]) % 10 - int(group['group_name'][0])
					if int(datetime.datetime.today().timetuple()[1]) >= 9:
						year += 1
					try:
						group_instance = Group.objects.get(group_number=group['group_name'])
						group_instance.year = year
						group_instance.save()
					except Group.DoesNotExist:
						group_instance = Group.objects.create(group_number=group['group_name'], year=year)
					days = get_as_list("https://mipt.ru/api/schedule/get_schedule?group_id=" + str(group['group_id']), 'days')
					for day in days:
						weekday = day['weekday']
						for lesson in day['lessons']:

							room, teacher, subject = None, None, None
							time_interval = 0

							if lesson['auditories']:
								room, created = Auditory.objects.get_or_create(name=lesson['auditories'][0]['auditory_name'])
							if lesson['teachers']:
								teacher, created = Teacher.objects.get_or_create(name=lesson['teachers'][0]['teacher_name'])
							if lesson['subject']:
								subject, created = Subject.objects.get_or_create(name=lesson['subject'])

							for k, v in rings.items():
								if rings[k] == lesson['time_start'] + ' - ' + lesson['time_end']:
									time_interval = k

							Lesson.objects.update_or_create(
								group=group_instance,
								weekday=weekday,
								time_interval=time_interval,
								defaults={
									'teacher': teacher, 'room': room, 'subject': subject,
								}
							)


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



