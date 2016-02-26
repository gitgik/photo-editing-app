from PIL import ImageFilter, ImageOps, ImageEnhance


def thumbnail(image):
    """Crop the image to the requested aspect ratio and size."""
    return ImageOps.fit(image, (100, 100))


def grayscale(image):
    """Return an image with a contrast of grey."""
    return ImageOps.grayscale(image)


def smooth(image):
    """Return a smoothened image."""
    return image.filter(ImageFilter.SMOOTH)


def sharpen(image):
    """Return a sharpened image."""
    return image.filter(ImageFilter.SHARPEN)


def detail(image):
    """Return an image with edge enhancement."""
    return image.filter(ImageFilter.EDGE_ENHANCE)


def flip(image):
    """Flip an image."""
    return ImageOps.invert(image)


def invert(image):
    """Invert an image."""
    return ImageOps.invert(image)


def mirror(image):
    """Flip the image horizontally."""
    return ImageOps.mirror(image)


def contrast(image):
    """Increase the contrast of an image and return the enhanced image."""
    photo = ImageEnhance.Contrast(image)
    return photo.enhance(1.5)


def blur(image):
    """Return a blur image using a gaussian blur filter."""
    return image.filter(ImageFilter.GaussianBlur(radius=3))


def brighten(image):
    """Return an image with a brightness enhancement factor of 1.5."""
    photo = ImageEnhance.Brightness(image)
    return photo.enhance(1.5)


def darken(image):
    """Return an image with a brightness enhancement factor of 0.5."""
    photo = ImageEnhance.Brightness(image)
    return photo.enhance(0.5)


def saturate(image):
    """Return an image with a saturation enhancement factor of 2.0 ."""
    photo = ImageEnhance.Color(image)
    return photo.enhance(2.0)


def charcoal(image):
    """Return an image with charcoal filter enhancements."""
    image = grayscale(image)
    image = contrast(image)
    image = brighten(image)
    image = detail(image)
    return image


photo_effects = [
    ('saturate', saturate),
    ('grayscale', grayscale),
    ('brighten', brighten),
    ('darken', darken),
    ('blur', blur),
    ('detail', detail),
    ('smooth', smooth),
    ('contrast', contrast),
    ('charcoal', charcoal),
    ('invert', invert),
    ('flip', flip),
    ('mirror', mirror),
]
