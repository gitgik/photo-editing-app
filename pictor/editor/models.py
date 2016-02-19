"""This file defines django models for editor app."""

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
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


class Photo(models.Model):
    """This model represents a photo record uploaded by the current user."""

    image = models.ImageField(upload_to=get_photo_path)
    caption = models.CharField(blank=True, maxlength=100)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False, auto_now=True)

    user = models.ForeignKey(User, related_name='photos')
