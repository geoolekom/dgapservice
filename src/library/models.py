from django.db import models


class Book(models.Model):

	def book_path(self, filename):
		return 'books/{0}'.format(filename)

	title = models.CharField(max_length=100, verbose_name='Название книги')
	book_file = models.FileField(verbose_name='Файл книги', upload_to=book_path)

	def __str__(self):
		return str(self.title)


class BookAuthor(models.Model):
	name = models.CharField(max_length=100, verbose_name='Имя')
	books = models.ManyToManyField(Book, blank=True, verbose_name='Книги автора')

	def __str__(self):
		return str(self.name)


class Subject(models.Model):
	name = models.CharField(max_length=100, verbose_name='Название')
	books = models.ManyToManyField(Book, blank=True, verbose_name='Книги по теме')

	def __str__(self):
		return str(self.name)

