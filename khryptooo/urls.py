from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    (r"^$", lambda r: HttpResponseRedirect("en/")),
    url(r'^en/', include('web_en.urls')),
    url(r'^jabber/', include('jabber.urls')),
)
