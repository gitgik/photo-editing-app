"""Define imports."""
from PIL import ImageFilter, ImageOps, ImageEnhance

temp_url = 'static/media/temp/'


def thumbnail(image, name):
    """Crop the image to the requested aspect ratio and size."""
    try:
        image.seek(0)
        photo = ImageOps.fit(image, (49, 49))
        photo.save(temp_url + "THUMBNAIL" + name)
        return temp_url + "THUMBNAIL" + name
    except IOError as e:
        return e.message


def grayscale(image, name):
    """Return an image with a contrast of grey."""
    try:
        image.seek(0)
        photo = ImageOps.grayscale(image)
        photo.save(temp_url + "GRAYSCALE" + name)
        return temp_url + "GRAYSCALE" + name
    except IOError as e:
        return e.message


def smooth(image, name):
    """Return a smoothened image."""
    try:
        image.seek(0)
        photo = image.filter(ImageFilter.SMOOTH)
        photo.save(temp_url + "SMOOTH" + name)
        return temp_url + "SMOOTH" + name
    except IOError as e:
        return e.message


def contour(image, name):
    """Return an image with a contour filter."""
    try:
        image.seek(0)
        photo = image.filter(ImageFilter.CONTOUR)
        photo.save(temp_url + "CONTOUR" + name)
        return temp_url + "CONTOUR" + name
    except IOError as e:
        return e.message


def sharpen(image, name):
    """Return a sharpened image."""
    try:
        image.seek(0)
        photo = image.filter(ImageFilter.SHARPEN)
        photo.save(temp_url + "SHARPEN" + name)
        return temp_url + "SHARPEN" + name
    except IOError as e:
        return e.message


def detail(image, name):
    """Return an image with edge enhancement."""
    try:
        image.seek(0)
        photo = image.filter(ImageFilter.EDGE_ENHANCE)
        photo.save(temp_url + "DETAIL" + name)
        return temp_url + "DETAIL" + name
    except IOError as e:
        return e.message


def flip(image, name):
    """Flip an image."""
    try:
        image.seek(0)
        photo = ImageOps.flip(image)
        photo.save(temp_url + "FLIP" + name)
        return temp_url + "FLIP" + name
    except IOError as e:
        return e.message


def invert(image, name):
    """Invert an image."""
    try:
        image.seek(0)
        photo = ImageOps.invert(image)
        photo.save(temp_url + "INVERT" + name)
        return temp_url + "INVERT" + name
    except IOError as e:
        return e.message


def mirror(image, name):
    """Flip the image horizontally."""
    try:
        image.seek(0)
        photo = ImageOps.mirror(image)
        photo.save(temp_url + "MIRROR" + name)
        return temp_url + "MIRROR" + name
    except IOError as e:
        return e.message


def contrast(image, name):
    """Increase the contrast of an image and return the enhanced image."""
    try:
        image.seek(0)
        photo = ImageEnhance.Contrast(image)
        photo = photo.enhance(1.5)
        photo.save(temp_url + "CONTRAST" + name)
        return temp_url + "CONTRAST" + name
    except IOError as e:
        return e.message


def blur(image, name):
    """Return a blur image using a gaussian blur filter."""
    try:
        image.seek(0)
        photo = image.filter(
            ImageFilter.GaussianBlur(radius=3))
        photo.save(temp_url + "BLUR" + name)
        return temp_url + "BLUR" + name
    except IOError as e:
        return e.message


def brighten(image, name):
    """Return an image with a brightness enhancement factor of 1.5."""
    try:
        image.seek(0)
        photo = ImageEnhance.Brightness(image)
        photo = photo.enhance(1.5)
        photo.save(temp_url + "BRIGHTEN" + name)
        return temp_url + "BRIGHTEN" + name
    except IOError as e:
        return e.message


def darken(image, name):
    """Return an image with a brightness enhancement factor of 0.5."""
    try:
        image.seek(0)
        photo = ImageEnhance.Brightness(image)
        photo = photo.enhance(0.5)
        photo.save(temp_url + "SATURATE" + name)
        return temp_url + "SATURATE" + name
    except IOError as e:
        return e.message


def saturate(image, name):
    """Return an image with a saturation enhancement factor of 2.0 ."""
    try:
        image.seek(0)
        photo = ImageEnhance.Color(image)
        photo = photo.enhance(2.0)
        photo.save(temp_url + "SATURATE" + name)
        return temp_url + "SATURATE" + name
    except IOError as e:
        return e.message
