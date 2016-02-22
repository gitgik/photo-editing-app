"""This file defines the urls for pictor app."""
from django.conf.urls import url, include
from views import LoginView, LogoutView, \
    DashboardView

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='index'),
    url(r'^account/', include('allauth.urls')),
    # url(r'^auth/facebook/$',
    #     FacebookAuthView.as_view(), name='facebook_auth'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^dashboard/$',
        DashboardView.as_view(), name='dashboard'),

]
