"""dgapservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
from feed.views import JsonPosts
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('feed:feed'))),
]

urlpatterns += i18n_patterns(
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^admin/', admin.site.urls),
    url(r'^feed/', include('feed.urls', namespace="feed")),
    url(r'^shedule/', include('shedule.urls', namespace='shedule')),
    url(r'^services/', include('services.urls', namespace='services')),
    url(r'^library/', include('library.urls', namespace='library')),
    url(r'^core/', include('core.urls', namespace='core')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^api/posts/', JsonPosts.as_view()),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
