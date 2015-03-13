from django.conf.urls import patterns, url
from web_en import views

urlpatterns = patterns("",
	url(r"^$", views.index, name="index"),
	url(r"^service-status/$", views.serviceStatus, name="serviceStatus"),
	url(r"^service/tor/$", views.torService, name="torService"),
)
