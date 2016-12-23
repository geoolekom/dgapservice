# coding: utf-8

from django.db import models
from groups.models import FacultyGroup as Group
from library.models import Subject
import datetime
from django.utils.translation import ugettext_lazy as _

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

weekdays = {
	1: _('Понедельник'),
	2: _('Вторник'),
	3: _('Среда'),
	4: _('Четверг'),
	5: _('Пятница'),
	6: _('Суббота'),
}


class Teacher(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return str(self.name)

	def get_link(self):
		return 'http://wikimipt.org/wiki/' + '_'.join(str(self.name).split(' '))

	def get_lessons(self):
		return Lesson.objects.filter(teacher=self)

	def get_subjects(self):
		lessons = self.get_lessons()
		subjects = []
		for lesson in lessons:
			if lesson not in subjects:
				subjects.append(lesson.subject)
		return subjects


class Auditory(models.Model):
	name = models.CharField(max_length=25)

	def __str__(self):
		return str(self.name)


class Lesson(models.Model):
	group = models.ForeignKey(Group, verbose_name='Группа')
	room = models.ForeignKey(Auditory, verbose_name='Аудитория', blank=True, null=True)
	teacher = models.ForeignKey(Teacher, verbose_name='Преподаватель', blank=True, null=True)
	subject = models.ForeignKey(Subject, verbose_name='Предмет', blank=True, null=True)

	pub_time = models.DateTimeField('Время публикации', auto_now_add=True)
	upd_time = models.DateTimeField('Последнее изменение', auto_now=True)

	def __str__(self):
		return str(self.group) + ": " + str(self.subject) + " в " + str(self.weekday)

	weekday = models.IntegerField(default=datetime.datetime.today().weekday(), verbose_name='День недели', choices=weekdays.items())
	time_interval = models.IntegerField(choices=rings.items(), blank=False, default=0, verbose_name='Время проведения')

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
								group_instance.subjects.add(subject)

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
