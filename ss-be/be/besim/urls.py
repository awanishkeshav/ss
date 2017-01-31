from django.conf.urls import url
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from rest_framework.urlpatterns import format_suffix_patterns

from besim import views

urlpatterns = [
	url(r'^besim/home$', views.besim_home),
	url(r'^besim/downloads$', views.besim_downloads),
]

urlpatterns += patterns('',
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)

handler404 = "views.besim_home"
