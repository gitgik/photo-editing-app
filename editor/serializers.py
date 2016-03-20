"""Define imports."""
from rest_framework import serializers
from .models import Photo, Effect


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer class for the Photo model."""

    class Meta:
        """This meta class defines the fields for photo serializer class."""

        model = Photo
        fields = ('id', 'image', 'name', 'date_created', 'date_modified',)
        read_only_fields = ('date_modified', 'date_created')


class PhotoEditSerializer(serializers.ModelSerializer):
    """Serializer class for the Photo model.

    Attributes:
        image_url: the image url from the server.
    """

    image_url = serializers.SerializerMethodField('generate_image_url')

    class Meta:
        """This meta class defines meta data for the serializer."""

        model = Photo
        fields = ('id', 'name', 'image', 'image_url', )

    def generate_image_url(self, obj):
        """Return absolute path of the image from the server."""
        return self.context['request'].build_absolute_uri(obj.image.url)


class EffectSerializer(serializers.ModelSerializer):
    """Serializer class for the Effects model."""

    class Meta:
        """This class defines meta data for the serializer."""

        model = Effect
        fields = ('id', 'effect', 'photo',)
