"""Test cases for pictor models."""
import StringIO
from django.test import TestCase
from django.db import IntegrityError

from faker import Factory
from django.contrib.auth.models import User
from editor.models import Photo, Effect, generate_uid
from PIL import Image

from mock import patch, MagicMock

fake = Factory.create()
# define extensions object
extensions = {
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'png': 'PNG',
    'gif': 'GIF'
}


def pil_to_django(image, ext):
    """Return a file in a format django understands."""
    fobject = StringIO.StringIO()
    image.save(fobject, format=extensions[ext.lower()])


class UserTestCase(TestCase):
    """Test for the user model."""

    def setUp(self):
        """Setup model for testing."""
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

    def tearDown(self):
        """Tear down the setup."""
        del self.user

    def test_user_is_created(self):
        """Test a user can be created."""
        self.assertIsInstance(self.user, User)

    def test_user_must_be_unique(self):
        """Test the creation of the same user fails."""
        try:
            self.user = User.objects.create_user(
                username=self.username, password=self.password)
        except IntegrityError as e:
            self.assertIn(
                "duplicate key value violates unique constraint", e.message)

    def test_uid_generation_for_photo(self):
        """Test a unique id is generated."""
        unique_id = generate_uid()
        self.assertIsNotNone(unique_id)


class PhotoTestCase(TestCase):
    """Test case for Photo model."""

    @patch('editor.models.Photo.save', MagicMock(name='save'))
    def setUp(self):
        """Set up for testing."""
        self.username = fake.user_name()
        self.password = fake.password()
        self.photo_name = 'test.png'
        image = Image.open('static/' + self.photo_name)
        self.image = pil_to_django(image, 'png')
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.created_image = Photo(
            image=self.image, name=self.photo_name, user=self.user)

    def test_image_is_created(self):
        """Test a photo is created."""
        self.assertEqual(self.created_image.name, self.photo_name)


class EffectTestCase(TestCase):
    """Test case for Effect model."""

    @patch('editor.models.Photo.save', MagicMock(name="save"))
    @patch('editor.models.Effect.save', MagicMock(name="save"))
    def setUp(self):
        """Set up for testing."""
        self.username = fake.user_name()
        self.password = fake.password()
        self.photo_name = 'test.png'
        image = Image.open('static/' + self.photo_name)
        self.image = pil_to_django(image, 'png')
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.created_image = Photo(
            image=self.image,
            name=self.photo_name,
            user=self.user)
        self.image_filters = Effect(
            effect=self.image,
            photo=self.created_image)

    def test_effect_creation(self):
        """Test a user can create an effect on a photo."""
        self.assertIsInstance(self.image_filters, Effect)
        self.assertEqual(self.image_filters.photo, self.created_image)
