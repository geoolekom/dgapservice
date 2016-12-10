from django.conf.urls import url
from shedule.views import *

urlpatterns = [
    url(r'^$', LessonListView.as_view(), name="shedule"),
    url(r'^lessons/edit/(?P<pk>\d+)', LessonUpdateView.as_view(), name="lesson-edit"),
]
