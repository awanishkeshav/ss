from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'be.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += [
    url(r'^', include('beapi.urls')),
	url(r'^', include('besim.urls')),
]
handler404 = "besim.views.besim_home"
