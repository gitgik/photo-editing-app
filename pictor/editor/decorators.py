"""This file defines decorators."""

# Apply update_wrapper to a wrapper function
from functools import wraps
from django.http import JsonResponse


def json_response(func):
    """View decorator that converts a dictionary response to json."""
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        status_code = response.get('status_code', 200)
        return JsonResponse(response, status=status_code)
    return func_wrapper
