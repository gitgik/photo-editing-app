"""This file defines the pictor forms."""
from django import forms
from django.contrib.auth.models import User
from models import SocialProfile, Photo


class FacebookAuthForm(forms.Form):
    """This form represents validating facebook user authentication data.

    Returns: User; either existing or newly created.
    """

    id = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    photo = forms.CharField(required=False)

    def save(self):
        """Save a social user with the form data."""
        data = self.cleaned_data
        user = None
        try:
            # Get the user if they already exist
            social_id = data['id']
            social_profile = SocialProfile.objects.get(
                provider=SocialProfile.FACEBOOK,
                social_id=social_id)
            user = social_profile.user

        except SocialProfile.DoesNotExist:
            # Create a new user
            user = User(
                username=data['id'],
                first_name=data['first_name'],
                last_name=data['last_name'])
            user.save()

            # Create and save the user's social profile
            user_social_profile = SocialProfile(
                provider=SocialProfile.FACEBOOK,
                social_id=data['id'],
                photo=data['photo'],
                user=user
            )
            user_social_profile.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            return user


class PhotoForm(forms.Form):
    """Form which handles photo uploads."""

    class Meta:
        models = Photo
        fields = ('image', 'caption', 'effects')

