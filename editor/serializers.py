"""Define imports."""
from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer class for the Photo model."""

    class Meta:
        """This meta class defines the fields for photo serializer class."""

        model = Photo
        fields = (
            'id', 'image', 'name', 'image_effect',
            'date_created', 'date_modified',
        )
        read_only_fields = ('date_modified', 'date_created')
