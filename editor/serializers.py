"""Define imports."""
from rest_framework import serializers
from .models import Photo, Effect


class Base64ImageField(serializers.ImageField):
    """A DRF field for handling image-upload through raw post data.

    It uses base64 for encoding and decoding the contents of the file.
    """

    def to_internal_value(self, data):
        """Import file content processors."""
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # retrieve the data from the base64 content
                data = data.split(';base64,')[1]

            # Try to decode the file. Returns validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name: 12 characters.
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        """Get the file extension of the decoded file."""
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


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


class EffectSerializer(serializers.ModelSerializer):
    """Serializer class for the Effects model."""

    effect = Base64ImageField(max_length=None, use_url=True,)

    class Meta:
        """This class defines meta data for the serializer."""

        model = Effect
        fields = ('id', 'effect', 'photo', 'date_created', 'date_edited',)
        read_only_fields = ('date_edited', 'date_created')
