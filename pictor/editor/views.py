"""Define the editor views."""
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth import login, logout

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from .enhancers import photo_effects
from PIL import Image, ImageEnhance, ImageDraw, ImageFont


from editor.serializers import PhotoSerializer
from editor.permissions import IsAuthenticated
from editor.models import Photo


class LoginView(View):
    """This view defines the login view."""

    def get(self, request, *args, **kwargs):
        """Render the index/login view."""
        if request.user.is_authenticated():
            return redirect(reverse('editor:dashboard'))

        context = {}
        context.update(csrf(self.request))
        return render(self.request, 'editor/index.html', context)


class PhotoListView(generics.ListCreateAPIView):
    """This view creates a photo uploaded from the client."""

    permission_classes = (IsAuthenticated, permissions.IsAuthenticated,)
    query_set = Photo.objects.all()
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        """Method that handles image upload and creation."""
        serializer = PhotoSerializer(
            data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PhotoDisplayView(APIView):
    """This view handles photo display for an authenticated user."""

    def get(self, request):
        """Return a photo specific data."""
        photo = Photo.objects.get(id=request.query_params['id'])

        context = {
            'request': request
        }
        serializer = PhotoSerializer(photo, context=context)
        return Response(serializer.data)

    def delete(self, request):
        """Delete an image."""
        pass


class LogoutView(View):
    """This View logs the authenticated user out."""

    def get(self, request, *args, **kwargs):
        """Flash user session and redirect them to login page."""
        logout(request)
        return redirect(reverse('editor:index'))


class PhotoUploadView(View):
    """View to handle image uploads from the authenticated user."""

    def post(self, request, *args, **kwargs):
        """Handle photo uploads."""
        pass
