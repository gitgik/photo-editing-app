"""Define the editor views."""
import os
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout
from allauth.socialaccount.models import SocialAccount

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from .enhancers import photo_effects

from editor.serializers import PhotoSerializer
from editor.permissions import IsAuthenticated
from editor.models import Photo
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def social_login(request):
    """View function for handling fb authentication."""
    if request.method == 'POST':
        access_token = request.data['accessToken']
        facebook_id = request.data['userID']
        if access_token:
            try:
                user = SocialAccount.objects.get(uid=facebook_id)
                avatar = str(user.get_avatar_url)
                if user:
                    return Response(
                        {
                            "profile_photo": avatar,
                            "extras": user.extra_data
                        },
                        status=status.HTTP_200_OK)
                else:
                    return Response("Bad credentials", status=403)
            except:
                return Response(
                    "Bad Request", status=status.HTTP_400_BAD_REQUEST)


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


class PhotoDetailView(APIView):
    """This view handles photo details anddisplay for an authenticated user."""

    def get(self, request):
        """Return a photo specific data."""
        photo = Photo.objects.get(id=request.query_params['id'])
        context = {
            'request': request
        }
        serializer = PhotoSerializer(photo, context=context)
        return Response(serializer.data)

    def delete(self, request):
        """Delete an image from both the db and the folder."""
        media_path = 'static/media/'
        photo = Photo.objects.get(id=request.query_params['id'])
        photo.delete()
        try:
            media_path += str(photo.image)
            os.remove(media_path)
        except:
            print("File not found")
        return Response(status=status.HTTP_204_NO_CONTENT)


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
