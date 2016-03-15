"""Test suite for social oauth."""
import os
from django.core.urlresolvers import reverse
from rest_framework import status
from django.test import TestCase


class OauthTestCase(TestCase):
    """Test case for social oauth login using facebook."""

    def test_login_with_access_token(self):
        """Test a user can get to the login page."""
        data = {
            'accessToken': os.getenv('ACCESS_TOKEN'),
            'backend': 'facebook'
        }
        response = self.client.post(reverse('editor:social_login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
