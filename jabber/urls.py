from django.conf.urls import patterns, url
from jabber import views

urlpatterns = patterns("",
	url(r"^register/$", views.register, name="register"),
)
