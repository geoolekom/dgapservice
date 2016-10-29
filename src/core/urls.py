from django.conf.urls import url
from core.views import RegisterView

urlpatterns = [
    url(r'^register/', RegisterView.as_view(), name="register")
]
