"""This file defines the urls for pictor app."""
from django.conf.urls import url, include
from views import LoginView

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='index'),
    url(r'^account/', include('allauth.urls')),
]
