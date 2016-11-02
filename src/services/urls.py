from django.conf.urls import url, include
from services.views import *

urlpatterns = [
	url(r'^print/', print_view, name="print"),
	url(r'^laundry/', laundry, name="laundry"),
	url(r'^food/', food, name="food"),
]