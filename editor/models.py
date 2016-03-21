"""This file defines django models for editor app."""

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from time import time
from hashids import Hashids
from django.conf import settings


def get_photo_path(instance, filename):
    """Define the upload path for saving the current user's photo to disk."""
    user_slug = "{}{}".format(
        instance.user.username,
        instance.user.id
    )
    upload_path = "photos/{}/{}".format(user_slug, filename)
    return upload_path


def get_effect_path(instance, filename):
    """Define the destination upload path for a saved effect."""
    upload_path = "effects/{}".format(filename)
    return upload_path


def generate_uid():
    """Generate a unique id using a custom salt, alphabet and min length."""
    salt = settings.SECRET_KEY
    alphabet = settings.UID_ALPHABET
    hashids = Hashids(salt=salt, alphabet=alphabet)
    unique_id = hashids.encode(int(time() * 1000))
    return unique_id


class Photo(models.Model):
    """This model represents photo records uploaded by the current user."""

    image = models.ImageField(upload_to=get_photo_path, max_length=255)
    name = models.CharField(default=generate_uid, max_length=255)
    image_effect = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False, auto_now=True)
    user = models.ForeignKey(User)


class Effect(models.Model):
    """This model represents the effects applied to a given image."""

    effect = models.ImageField(upload_to=get_effect_path, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(editable=False, auto_now=True)
    photo = models.ForeignKey(Photo)
