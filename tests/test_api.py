"""Test cases for picto api."""

import StringIO
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.core.files import File
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
        self.image_url = 'static/test.png'

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
        image_name = 'test.png'
        with open(self.image_url, 'rb') as image:
            data = {'image': image, 'name': image_name}
            response = self.client.post(reverse('editor:photos'), data)
            image.close()
        response = self.client.get(reverse('editor:photos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test data retrieved
        data = [i.values() for i in response.data]
        self.assertIn(
            u'{}'.format(self.photo_name),
            data[0])

    def test_getting_photo_by_id(self):
        """Test a given photo can be retrieved using the photoID."""
        self.created_image = Photo(
            image=self.image,
            name=self.photo_name, user=self.user)
        self.created_image.save()
        rv = self.client.get(
            '/api/edit_photo/?id={}'.format(self.created_image.id))
        self.assertEqual(rv.status_code, status.HTTP_200_OK)
        self.assertEqual(rv.data.get('name'), self.created_image.name)

    def test_user_can_edit_photo(self):
        """Test a given photo can be edited."""
        self.name = 'test.png'
        self.image = File(open('static/test.jpg', 'rb'))
        self.created_image = Photo(
            image=self.image,
            name=self.name, user=self.user)
        self.created_image.save()
        response = self.client.get(reverse('editor:photos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'id': self.created_image.id,
            'image': self.created_image.image,
            'name': 'the new picture'
        }
        rv = self.client.put('/api/edit_photo/', data=data)
        self.assertEqual(rv.status_code, status.HTTP_200_OK)

        # test actual data of edited photo
        rv = self.client.get(
            '/api/edit_photo/?id={}'.format(self.created_image.id))
        self.assertContains(rv, data['name'], status_code=200)

    def test_user_can_delete_photo(self):
        """Test a given photo can be deleted."""
        self.name = 'test.png'
        self.image = File(open('static/test.jpg', 'rb'))
        self.created_image = Photo(
            image=self.image,
            name=self.name, user=self.user)
        self.created_image.save()
        response = self.client.get(reverse('editor:photos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rv = self.client.delete(
            '/api/edit_photo/?id={}'.format(self.created_image.id))
        self.assertEqual(rv.status_code, status.HTTP_204_NO_CONTENT)

    def test_filters_request_of_invalid_image(self):
        """Test correct server response when an IO error occurs."""
        invalid_data = {
            'imageID': 300
        }
        response = self.client.get(reverse('editor:filters'), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MockResponse(object):
    """Mock response class."""

    def __init__(self, response_data, code=200):
        """init."""
        self.response_data = response_data
        self.code = code
        self.headers = {'content-type': 'text/plain; charset=utf-8'}

    def read(self):
        """Read data from response."""
        return self.response_data

    def getcode(self):
        """Get response http code."""
        return self.code


class ImageEffectsTestCase(APITestCase):
    """Test case for Image effects."""

    def setUp(self):
        """Set up a mock for opening actual file url."""
        self.patcher = patch('urllib2.urlopen')
        self.urlopen_mock = self.patcher.start()

        self.username = fake.user_name()
        self.password = fake.password()

        self.photo_name = 'test.png'
        self.image_url = 'static/test.png'

        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.user = authenticate(
            username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_application_of_filters(self):
        """Test that filters can be applied to images."""
        self.name = 'test.png'
        self.image = File(open('static/test.png', 'rb'))
        self.created_image = Photo(
            image=self.image,
            name=self.name, user=self.user)
        self.created_image.save()
        data = {
            'imageID': self.created_image.id
        }
        self.urlopen_mock.return_value = MockResponse(data)
        response = self.client.get(reverse('editor:filters'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image_effects_deletion(self):
        """Test deletion of image effects from the server."""
        self.name = 'test.png'
        self.image = File(open('static/test.png', 'rb'))
        self.created_image = Photo(
            image=self.image,
            name=self.name, user=self.user)
        self.created_image.save()
        data = {
            'imageID': self.created_image.id
        }
        self.urlopen_mock.return_value = MockResponse(data)
        response = self.client.get(reverse('editor:filters'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # actual deletion
        data = {'id': self.created_image.pk, 'image_url': ''}
        rv = self.client.post(reverse('editor:remove_effects'), data)
        self.assertEqual(rv.status_code, status.HTTP_200_OK)

    def tearDown(self):
        """Tear down."""
        self.patcher.stop()
