"""Define the editor views."""
import os
# from io import BytesIO
import requests
from urllib2 import urlopen
from StringIO import StringIO

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from editor import photo_effects
from editor.serializers import PhotoSerializer
from editor.permissions import Authenticate
from editor.models import Photo
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login
from social.apps.django_app.utils import load_strategy, load_backend
from social.exceptions import AuthAlreadyAssociated


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def social_login(request):
    """View function for handling fb authentication."""
    if request.method == 'POST':
        access_token = request.data['accessToken']
        backend = request.data['backend']
        print access_token
        if access_token:
            strategy = load_strategy(request)
            backend = load_backend(
                strategy=strategy, name=backend, redirect_uri=None)
            try:
                user = backend.do_auth(access_token)
            except AuthAlreadyAssociated:
                return Response(
                    {"errors": "This social account is already in use"},
                    status=status.HTTP_400_BAD_REQUEST)
            if user:
                login(request, user)
                return Response(
                    {'user': user.username}, status=status.HTTP_200_OK)
            else:
                return Response("Bad credentials", status=403)
        else:
            return Response("Bad request", status=400)


@api_view(['GET'])
def filters(request):
    """View handles the filters on a given photo."""
    if request.method == 'GET':
        image_url = request.query_params['image_url']
        photo_name = image_url.rsplit('/', 1)[-1]
        photo = requests.get(image_url)
        photo_file = photo.content
        # print photo.headers['content-length']
        # photo.raw.decode_content = True
        # photo_file = io.BytesIO(photo_file)
        # image = urlopen(image_url)
        # photo_file = io.BytesIO(image.read())
        photo_file = StringIO(photo_file)
        # photo_file.seek(0)
        data = {
            'BLUR': photo_effects.blur(photo_file, photo_name),
            'GRAY': photo_effects.grayscale(photo_file, photo_name),

            'SMOOTH': photo_effects.smooth(photo_file, photo_name),
            'SHARP': photo_effects.sharpen(photo_file, photo_name),
            'DETAIL': photo_effects.detail(photo_file, photo_name),
            'CONTRAST': photo_effects.contrast(photo_file, photo_name),
            'BRIGHT': photo_effects.brighten(photo_file, photo_name),
            'DARK': photo_effects.darken(photo_file, photo_name),
            'FLIP': photo_effects.flip(photo_file, photo_name),
            'CONTOUR': photo_effects.contour(photo_file, photo_name),
            'THERMAL': photo_effects.invert(photo_file, photo_name),
            'SATURATE': photo_effects.saturate(photo_file, photo_name),
            'MIRROR': photo_effects.mirror(photo_file, photo_name),
        }

        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def remove_effects(request):
    """View allows resetting back from filters."""
    if request.method == 'GET':
        temp_url = 'static/media/temp/'
        file_list = os.listdir(temp_url)
        for file_name in file_list:
            os.remove(temp_url + "/" + file_name)

        return Response(status=status.HTTP_200_OK)


class PhotoListView(generics.ListCreateAPIView):
    """This view creates a photo uploaded from the client."""

    permission_classes = (Authenticate, permissions.IsAuthenticated,)
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        """Method that handles image upload and creation."""
        serializer = PhotoSerializer(
            data=self.request.data, context={'request': self.request})
        # import pdb; pdb.set_trace()
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """Method to return photos of logged in user."""
        user = self.request.user
        return Photo.objects.filter(user=user)


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
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
