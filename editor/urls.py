"""This file defines the urls for pictor app."""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# from views import LoginView
from editor import views

urlpatterns = [
    url(r'^login/', views.social_login, name='social_login'),
    url(r'^photos/', views.PhotoListView.as_view(), name='photos'),
    url(r'^filters/', views.filters, name="filters"),
    url(r'^photo_effects/', views.handle_photo_effects, name="photo_effects"),
    url(r'^remove_effects/', views.remove_effects, name="remove_effects"),
    url(r'^edit_photo/', views.PhotoDetailView.as_view(), name='editphoto'),
    url(r'^logout/', 'django.contrib.auth.views.logout', name='logout')
]

urlpatterns = format_suffix_patterns(urlpatterns)
