"""Define imports."""
from PIL import ImageFilter, ImageOps, ImageEnhance


def grayscale(image, name, temp_url):
    """Return an image with a contrast of grey."""
    image.seek(0)
    photo = ImageOps.grayscale(image)
    photo.save(temp_url + "GRAYSCALE" + name)
    return temp_url + "GRAYSCALE" + name


def smooth(image, name, temp_url):
    """Return a smoothened image."""
    image.seek(0)
    photo = image.filter(ImageFilter.SMOOTH)
    photo.save(temp_url + "SMOOTH" + name)
    return temp_url + "SMOOTH" + name


def contour(image, name, temp_url):
    """Return an image with a contour filter."""
    image.seek(0)
    photo = image.filter(ImageFilter.CONTOUR)
    photo.save(temp_url + "CONTOUR" + name)
    return temp_url + "CONTOUR" + name


def sharpen(image, name, temp_url):
    """Return a sharpened image."""
    image.seek(0)
    photo = image.filter(ImageFilter.SHARPEN)
    photo.save(temp_url + "SHARPEN" + name)
    return temp_url + "SHARPEN" + name


def detail(image, name, temp_url):
    """Return an image with edge enhancement."""
    image.seek(0)
    photo = image.filter(ImageFilter.EDGE_ENHANCE)
    photo.save(temp_url + "DETAIL" + name)
    return temp_url + "DETAIL" + name


def flip(image, name, temp_url):
    """Flip an image."""
    image.seek(0)
    photo = ImageOps.flip(image)
    photo.save(temp_url + "FLIP" + name)
    return temp_url + "FLIP" + name


def invert(image, name, temp_url):
    """Invert an image."""
    image.seek(0)
    photo = ImageOps.invert(image)
    photo.save(temp_url + "INVERT" + name)
    return temp_url + "INVERT" + name


def mirror(image, name, temp_url):
    """Flip the image horizontally."""
    image.seek(0)
    photo = ImageOps.mirror(image)
    photo.save(temp_url + "MIRROR" + name)
    return temp_url + "MIRROR" + name


def contrast(image, name, temp_url):
    """Increase the contrast of an image and return the enhanced image."""
    image.seek(0)
    photo = ImageEnhance.Contrast(image)
    photo = photo.enhance(1.5)
    photo.save(temp_url + "CONTRAST" + name)
    return temp_url + "CONTRAST" + name


def blur(image, name, temp_url):
    """Return a blur image using a gaussian blur filter."""
    image.seek(0)
    photo = image.filter(
        ImageFilter.GaussianBlur(radius=3))
    photo.save(temp_url + "BLUR" + name)
    return temp_url + "BLUR" + name


def brighten(image, name, temp_url):
    """Return an image with a brightness enhancement factor of 1.5."""
    image.seek(0)
    photo = ImageEnhance.Brightness(image)
    photo = photo.enhance(1.5)
    photo.save(temp_url + "BRIGHTEN" + name)
    return temp_url + "BRIGHTEN" + name


def darken(image, name, temp_url):
    """Return an image with a brightness enhancement factor of 0.5."""
    image.seek(0)
    photo = ImageEnhance.Brightness(image)
    photo = photo.enhance(0.5)
    photo.save(temp_url + "SATURATE" + name)
    return temp_url + "SATURATE" + name


def saturate(image, name, temp_url):
    """Return an image with a saturation enhancement factor of 2.0 ."""
    image.seek(0)
    photo = ImageEnhance.Color(image)
    photo = photo.enhance(2.0)
    photo.save(temp_url + "SATURATE" + name)
    return temp_url + "SATURATE" + name
