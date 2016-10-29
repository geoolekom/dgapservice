# coding: utf-8

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from groups.models import FacultyGroup as Group
from dgapservice.settings import STATIC_ROOT


import os
import xlrd


class Shedule(models.Model):
	group = models.ForeignKey(Group)
	day_of_week = models.IntegerField(default=1, validators=[
		MaxValueValidator(7),
		MinValueValidator(1)
	])
	lesson_number = models.IntegerField(default=1, validators=[
		MaxValueValidator(7),
		MinValueValidator(1)
	])
	lesson_title = models.CharField(max_length=50)
	teacher = models.CharField(max_length=50)
	room = models.CharField(max_length=10)

	def __str__(self):
		return str(self.group) + ": day " + str(self.day_of_week) + ", lesson " + str(self.lesson_number) + '.\t' + str(self.lesson_title)

	@staticmethod
	def refill():
		os.chdir(STATIC_ROOT + 'shedule/xls')
		files = os.listdir()
		for file_name in files:
			book = xlrd.open_workbook(file_name,formatting_info=True)
			sheet = book.sheet_by_index(0)

			day_of_week = 1
			lesson_number = 0

			for row_number in range(sheet.nrows):

				row = sheet.row_values(row_number)
				if row_number == 4:
					groups = dict()
					for i in range(len(row)):
						if row[i].isnumeric():
							groups[i] = int(row[i])
				elif row_number > 4:
					print(row[0], row[1], '\tand\t', day_of_week, lesson_number)
					if row[1] != '':
						lesson_number += 1
					if lesson_number == 8:
						lesson_number = 1
						day_of_week += 1

					for i in range(2, len(row)):
						try:
							group_number = groups[i]
							group, created = Group.objects.get_or_create(group_number=group_number, year=2016)

							if row[i] == '' and row[1] != '':
								lesson_title = ''
								teacher = ''
								room = ''
								shedule = Shedule(group=group,
									day_of_week=day_of_week,
									lesson_number=lesson_number,
									lesson_title=lesson_title,
									teacher=teacher,
									room=room)
								shedule.save()
							else:
								if len(row[i].split('/')) >= 3:
									lesson_title, teacher, room = row[i].split('/')
								elif len(row[i].split(' ')) >= 3 and row[i].split(' ')[-2].isnumeric():
									lesson_title = ' '.join(row[i].split(' ')[:-2])
									room = ' '.join(row[i].split(' ')[-2:])
									teacher = ''
								else:
									lesson_title = row[i]
									teacher = ''
									room = ''

								try:
									Shedule.objects.filter(group=group, day_of_week=day_of_week, lesson_number=lesson_number).delete()
									Shedule.objects.create(group=group,
										day_of_week=day_of_week,
										lesson_number=lesson_number,
										lesson_title=lesson_title,
										teacher=teacher,
										room=room)
								except:
									shedule = Shedule(group=group, 
										day_of_week=day_of_week,
										lesson_number=lesson_number,
										lesson_title=lesson_title,
										teacher=teacher,
										room=room)
									shedule.save()
						except:
							pass


