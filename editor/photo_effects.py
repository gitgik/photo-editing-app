"""Define imports."""
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

temp_url = 'static/media/temp/'


def thumbnail(image, name):
    """Crop the image to the requested aspect ratio and size."""
    photo = Image.open(image)
    photo = ImageOps.fit(photo, (49, 49))
    photo.save(temp_url + "THUMBNAIL" + name)
    return temp_url + "THUMBNAIL" + name


def grayscale(image, name):
    """Return an image with a contrast of grey."""
    photo = Image.open(image)
    photo = ImageOps.grayscale(photo)
    photo.save(temp_url + "GRAYSCALE" + name)
    return temp_url + "GRAYSCALE" + name


def smooth(image, name):
    """Return a smoothened image."""
    photo = Image.open(image)
    photo = photo.filter(ImageFilter.SMOOTH)
    photo.save(temp_url + "SMOOTH" + name)
    return temp_url + "SMOOTH" + name


def contour(image, name):
    """Return an image with a contour filter."""
    photo = Image.open(image)
    photo = photo.filter(ImageFilter.CONTOUR)
    photo.save(temp_url + "CONTOUR" + name)
    return temp_url + "CONTOUR" + name


def sharpen(image, name):
    """Return a sharpened image."""
    photo = Image.open(image)
    photo = photo.filter(ImageFilter.SHARPEN)
    photo.save(temp_url + "SHARPEN" + name)
    return temp_url + "SHARPEN" + name


def detail(image, name):
    """Return an image with edge enhancement."""
    photo = Image.open(image)
    photo = photo.filter(ImageFilter.EDGE_ENHANCE)
    photo.save(temp_url + "DETAIL" + name)
    return temp_url + "DETAIL" + name


def flip(image, name):
    """Flip an image."""
    photo = Image.open(image)
    photo = ImageOps.flip(photo)
    photo.save(temp_url + "FLIP" + name)
    return temp_url + "FLIP" + name


def invert(image, name):
    """Invert an image."""
    photo = Image.open(image)
    photo = ImageOps.invert(photo)
    photo.save(temp_url + "INVERT" + name)
    return temp_url + "INVERT" + name


def mirror(image, name):
    """Flip the image horizontally."""
    photo = Image.open(image)
    photo = ImageOps.mirror(photo)
    photo.save(temp_url + "MIRROR" + name)
    return temp_url + "MIRROR" + name


def contrast(image, name):
    """Increase the contrast of an image and return the enhanced image."""
    photo = Image.open(image)
    photo = ImageEnhance.Contrast(photo)
    photo = photo.enhance(1.5)
    photo.save(temp_url + "CONTRAST" + name)
    return temp_url + "CONTRAST" + name


def blur(image, name):
    """Return a blur image using a gaussian blur filter."""
    photo = Image.open(image)
    photo = photo.filter(ImageFilter.GaussianBlur(radius=3))
    photo.save(temp_url + "BLUR" + name)
    return temp_url + "BLUR" + name


def brighten(image, name):
    """Return an image with a brightness enhancement factor of 1.5."""
    photo = Image.open(image)
    photo = ImageEnhance.Brightness(photo)
    photo = photo.enhance(1.5)
    photo.save(temp_url + "BRIGHTEN" + name)
    return temp_url + "BRIGHTEN" + name


def darken(image, name):
    """Return an image with a brightness enhancement factor of 0.5."""
    photo = Image.open(image)
    photo = ImageEnhance.Brightness(photo)
    photo = photo.enhance(0.5)
    photo.save(temp_url + "SATURATE" + name)
    return temp_url + "SATURATE" + name


def saturate(image, name):
    """Return an image with a saturation enhancement factor of 2.0 ."""
    photo = Image.open(image)
    photo = ImageEnhance.Color(photo)
    photo = photo.enhance(2.0)
    photo.save(temp_url + "SATURATE" + name)
    return temp_url + "SATURATE" + name
