from django.conf.urls import url, include
from library.views import BookListView

urlpatterns = [
	url(r'^$', BookListView.as_view(), name='library')
]