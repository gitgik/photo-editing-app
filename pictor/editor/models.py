"""This file defines django models for editor app."""

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from time import time
from hashids import Hashids
from django.conf import settings
import os


def get_photo_path(instance, filename):
    """Define the upload path for saving the current user's photo to disk."""
    name, ext = os.path.splitext(filename)
    new_name = '{}{}'.format(instance.public_id, ext)
    user_slug = "{}{}".format(
        instance.user.username,
        instance.user.id
    )
    upload_path = "photos/{}/{}".format(user_slug, new_name)
    return upload_path


def generate_uid():
    """Generate a unique id."""
    salt = settings.SECRET_KEY
    min_length = settings.UID_LENGTH,
    alphabet = settings.UID_ALPHABET
    hashids = Hashids(salt=salt, min_length=min_length, alphabet=alphabet)
    unique_id = hashids.encode(int(time() * 1000))
    return unique_id


class Photo(models.Model):
    """This model represents a photo record uploaded by the current user."""

    image = models.ImageField(upload_to=get_photo_path, max_length=255)
    public_id = models.CharField(default=generate_uid, max_length=50)
    caption = models.CharField(blank=True, max_length=255)
    effects = models.CharField(blank=True, max_length=255)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_edited = models.DateTimeField(editable=False, auto_now=True)

    user = models.ForeignKey(User, related_name='photos')
