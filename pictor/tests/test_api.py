"""Test cases for pictor."""

import StringIO
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.test import APITestCase
from editor.models import Photo
from faker import Factory
from PIL import Image
from mock import MagicMock, patch

# define extensions object
extensions = {
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'png': 'PNG',
    'gif': 'GIF'
}
fake = Factory.create()


def pil_to_django(image, ext):
        """Return a file in a format django understands."""
        fobject = StringIO.StringIO()
        image.save(fobject, format=extensions[ext.lower()])
        return ContentFile(fobject.getvalue())


class UserPhotoTestCase(APITestCase):
    """Test user login."""

    def setUp(self):
        """Set up user data."""
        self.username = fake.user_name()
        self.password = fake.password()

        self.photo_name = 'test.png'
        self.image_url = 'static/media/test.png'

        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.user = authenticate(
            username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # get the image ready for loading
        self.image = Image.frombytes('L', (100, 100), "\x00" * 100 * 100)
        self.image = pil_to_django(self.image, 'png')
        self.image_create = Photo(
            image=self.image, name=self.photo_name, user=self.user).save()

    def tearDown(self):
        """Tear down all things test_user."""
        del self.user
        del self.image_create

    @patch('editor.models.Photo.save', MagicMock(name="save"))
    def test_user_photo_creation(self):
        """Test photo creation by a given user."""
        image_name = 'test.png'
        with open(self.image_url, 'rb') as image:
            data = {'image': image, 'name': image_name}
            response = self.client.post(reverse('editor:photos'), data)
            image.close()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), image_name)

    def test_photo_retrievals(self):
        """Test user can retrieve their photos."""
        response = self.client.get(reverse('editor:photos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test data retrieved
        data = [i.values() for i in response.data]
        self.assertIn(
            u'{}'.format(self.photo_name),
            data[0])
