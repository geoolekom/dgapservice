from django.conf.urls import url
from core.views import *
from django.contrib.auth.views import login, logout
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^register/', RegisterView.as_view(), name="register"),
    url(r'^login/', login, {'template_name': 'core/user.html'}, name="login"),
    url(r'^logout/', logout, {'next_page': '/feed'}, name="logout"),
    url(r'^upload/', csrf_exempt(UploadView.as_view())),
]
