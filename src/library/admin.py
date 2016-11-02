from django.contrib import admin
from library.models import Book, BookAuthor, Subject

admin.site.register(Book)
admin.site.register(BookAuthor)
admin.site.register(Subject)
