"""Define imports."""
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

temp_url = 'static/media/temp/'


def thumbnail(image, name):
    """Crop the image to the requested aspect ratio and size."""
    try:
        with Image.open(image) as photo:
            photo.seek(0)
            photo = ImageOps.fit(photo, (49, 49))
            photo.save(temp_url + "THUMBNAIL" + name)
        return temp_url + "THUMBNAIL" + name
    except IOError as e:
        print "PICTOR ERROR: {}".format(e)


def grayscale(image, name):
    """Return an image with a contrast of grey."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image, mode='r') as photo:
            photo.seek(0)
            photo = ImageOps.grayscale(photo)
            photo.save(temp_url + "GRAYSCALE" + name)
        return temp_url + "GRAYSCALE" + name
    except IOError as e:
        print "DID NOT WORK {}".format(e)


def smooth(image, name):
    """Return a smoothened image."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = photo.filter(ImageFilter.SMOOTH)
            photo.save(temp_url + "SMOOTH" + name)
        return temp_url + "SMOOTH" + name
    except IOError as e:
        print (e)


def contour(image, name):
    """Return an image with a contour filter."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = photo.filter(ImageFilter.CONTOUR)
            photo.save(temp_url + "CONTOUR" + name)
        return temp_url + "CONTOUR" + name
    except IOError as e:
        print (e)


def sharpen(image, name):
    """Return a sharpened image."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = photo.filter(ImageFilter.SHARPEN)
            photo.save(temp_url + "SHARPEN" + name)
        return temp_url + "SHARPEN" + name
    except IOError as e:
        print (e)


def detail(image, name):
    """Return an image with edge enhancement."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = photo.filter(ImageFilter.EDGE_ENHANCE)
            photo.save(temp_url + "DETAIL" + name)
        return temp_url + "DETAIL" + name
    except IOError as e:
        print (e)


def flip(image, name):
    """Flip an image."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = ImageOps.flip(photo)
            photo.save(temp_url + "FLIP" + name)
        return temp_url + "FLIP" + name
    except IOError as e:
        print (e)


def invert(image, name):
    """Invert an image."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = ImageOps.invert(photo)
            photo.save(temp_url + "INVERT" + name)
        return temp_url + "INVERT" + name
    except IOError as e:
        print (e)


def mirror(image, name):
    """Flip the image horizontally."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = ImageOps.mirror(photo)
            photo.save(temp_url + "MIRROR" + name)
        return temp_url + "MIRROR" + name
    except IOError as e:
        print (e)


def contrast(image, name):
    """Increase the contrast of an image and return the enhanced image."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = ImageEnhance.Contrast(photo)
            photo = photo.enhance(1.5)
            photo.save(temp_url + "CONTRAST" + name)
        return temp_url + "CONTRAST" + name
    except IOError as e:
        print (e)


def blur(image, name):
    """Return a blur image using a gaussian blur filter."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = photo.filter(
                ImageFilter.GaussianBlur(radius=3))
            photo.save(temp_url + "BLUR" + name)
        return temp_url + "BLUR" + name
    except IOError as e:
        print (e)


def brighten(image, name):
    """Return an image with a brightness enhancement factor of 1.5."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = ImageEnhance.Brightness(photo)
            photo = photo.enhance(1.5)
            photo.save(temp_url + "BRIGHTEN" + name)
        return temp_url + "BRIGHTEN" + name
    except IOError as e:
        print (e)


def darken(image, name):
    """Return an image with a brightness enhancement factor of 0.5."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = ImageEnhance.Brightness(photo)
            photo = photo.enhance(0.5)
            photo.save(temp_url + "SATURATE" + name)
        return temp_url + "SATURATE" + name
    except IOError as e:
        print (e)


def saturate(image, name):
    """Return an image with a saturation enhancement factor of 2.0 ."""
    try:
        print "SEEKING IMAGE BACK TO ZERO"
        image.seek(0)
        with Image.open(image) as photo:
            photo.seek(0)
            photo = ImageEnhance.Color(photo)
            photo = photo.enhance(2.0)
            photo.save(temp_url + "SATURATE" + name)
    except IOError as e:
        print (e)
    return temp_url + "SATURATE" + name
