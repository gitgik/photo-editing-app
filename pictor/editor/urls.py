"""This file defines the urls for pictor app."""
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from views import LoginView
from editor import views

urlpatterns = [
    url(r'^', LoginView.as_view(), name='index'),
    url(r'^account/', include('allauth.urls')),
    url(r'^photos/', views.PhotoListView.as_view(), name='photos'),
    url(r'^edit_photo/', views.PhotoDetailView.as_view(), name='editphoto'),
    url(r'logout/', 'django.contrib.auth.views.logout', name='logout')
]

urlpatterns = format_suffix_patterns(urlpatterns)
