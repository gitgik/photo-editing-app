"""This file defines the urls for pictor app."""
from django.conf.urls import url
from views import LoginView, FacebookAuthView, LogoutView

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='index'),
    url(r'^auth/facebook/$', FacebookAuthView.as_view(), name='facebook_auth'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
