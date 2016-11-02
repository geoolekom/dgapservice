from django.conf.urls import url
from shedule.views import *

urlpatterns = [
    url(r'^$', SheduleListView.as_view(), name="shedule"),
    url(r'^edit-lesson', edit_shedule, name="edit_shedule")
]
