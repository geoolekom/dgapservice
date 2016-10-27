from django.conf.urls import url
from shedule.views import SheduleListView

urlpatterns = [
    url(r'^$', SheduleListView.as_view(), name="shedule")
]
