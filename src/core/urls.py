from django.conf.urls import url
from core.views import RegisterView
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^register/', RegisterView.as_view(), name="register"),
    url(r'^login/', login, {'template_name': 'core/user.html'}, name="login"),
    url(r'^logout/', logout, {'next_page': '/feed'}, name="logout"),
]
