"""Test cases for pictor models."""
from django.test import TestCase
from django.db import IntegrityError

from faker import Factory
from django.contrib.auth.models import User
from editor.models import Photo, Effect
from PIL import Image

from mock import patch, MagicMock

fake = Factory.create()


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
