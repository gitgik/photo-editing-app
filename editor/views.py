"""Define the editor views."""
import os
# import base64
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
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
        image_id = request.query_params['imageID']
        try:
            photo_obj = Photo.objects.get(id=image_id)
            photo_name = photo_obj.name
            # check to see if image has a saved effect
            input_image = photo_obj.image_effect if photo_obj.image_effect \
                else photo_obj.image
            photo_file = Image.open(input_image)
            temp_url = 'static/media/temp/{}/'.format(image_id)
            if not os.path.isdir(temp_url):
                os.makedirs(temp_url)

            data = {
                'BLUR': photo_effects.blur(
                    photo_file, photo_name, temp_url),
                'BRIGHT': photo_effects.brighten(
                    photo_file, photo_name, temp_url),
                'CONTOUR': photo_effects.contour(
                    photo_file, photo_name, temp_url),
                'CONTRAST': photo_effects.contrast(
                    photo_file, photo_name, temp_url),
                'DARK': photo_effects.darken(
                    photo_file, photo_name, temp_url),
                'DETAIL': photo_effects.detail(
                    photo_file, photo_name, temp_url),
                'FLIP': photo_effects.flip(
                    photo_file, photo_name, temp_url),
                'GRAY': photo_effects.grayscale(
                    photo_file, photo_name, temp_url),
                'MIRROR': photo_effects.mirror(
                    photo_file, photo_name, temp_url),
                'SMOOTH': photo_effects.smooth(
                    photo_file, photo_name, temp_url),
                'SHARP': photo_effects.sharpen(
                    photo_file, photo_name, temp_url),
                'SATURATE': photo_effects.saturate(
                    photo_file, photo_name, temp_url),
            }
            return Response(data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(
                "Bad request",
                status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def remove_effects(request):
    """View allows resetting back from filters."""
    if request.method == 'POST':
        temp_url = 'static/media/temp/{}/'.format(request.data['id'])
        exception_photo = request.data['image_url']
        try:
            file_list = os.listdir(temp_url)
            persist = exception_photo.split('/')[-1]
            for file_name in file_list:
                if persist in file_name:
                    continue
                os.remove(temp_url + file_name)
            return Response(status=status.HTTP_200_OK)
        except OSError:
            return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoListView(generics.ListCreateAPIView):
    """This view creates a photo uploaded from the client."""

    permission_classes = (Authenticate, permissions.IsAuthenticated,)
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        """Method that handles image upload and creation."""
        serializer = PhotoSerializer(
            data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """Method to return photos of logged in user."""
        user = self.request.user
        queryset = Photo.objects.filter(user=user)
        return queryset


class PhotoDetailView(APIView):
    """This view handles photo details for an authenticated user."""

    def get(self, request):
        """Return a photo specific data."""
        photo_obj = Photo.objects.get(id=request.query_params['id'])
        context = {
            'request': request
        }
        serializer = PhotoSerializer(photo_obj, context=context)
        return Response(serializer.data)

    def put(self, request):
        """Edit the image."""
        if request.data['image_effect'] == "":
            try:
                photo = Photo.objects.get(id=request.data['id'])
                request.data['image'] = photo.image
            except ObjectDoesNotExist as e:
                return Response(e.message, status.HTTP_400_BAD_REQUEST)
        else:
            try:
                photo = Photo.objects.get(id=request.data['id'])
                request.data['image'] = photo.image
                image_url = request.data['image_effect']
                image_name = image_url.split('/')[-1]
                image_path = image_url.split(':8000/')[-1]
                effect_path = "static/media/photos/{}{}/effects/".format(
                    request.user.username, request.user.id)
                # create the directory for saving effects
                if not os.path.isdir(effect_path):
                    os.makedirs(effect_path)
                image = Image.open(image_path)
                image.save(effect_path + image_name)
                # replace the custom effect path with the one from the client
                if (request.user.username in image_path):
                    request.data['image_effect'] = ''
                else:
                    request.data['image_effect'] = effect_path + image_name
            except IOError as e:
                return Response(e.message, status.HTTP_400_BAD_REQUEST)

        serializer = PhotoSerializer(
            photo, data=request.data,
            context={'request': self.request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print serializer.errors
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete an image from both the db and the folder."""
        media_path = 'static/media/'
        effect_path = 'static/effects/'
        photo = Photo.objects.get(id=request.query_params['id'])

        try:
            photo.delete()
            media_path += str(photo.image)
            effect_path += str(photo.image_effect)
            os.remove(media_path)
            os.remove(effect_path)
        except OSError:
            print "Could not remove image files from server"
        return Response(status=status.HTTP_204_NO_CONTENT)
