import os


def facebook_app_id(request):
    """Return a context containing the facebook app id."""
    context = {
        'facebook_app_id': os.getenv("FACEBOOK_APP_ID"),
    }
    return context
