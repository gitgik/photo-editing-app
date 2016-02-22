"""This file defines decorators."""

# Apply update_wrapper to a wrapper function
from functools import wraps
from django.http import JsonResponse
from django.core import serializers


def json_response(func):
    """View decorator that converts a dictionary response to json."""
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        func_response = func(request, *args, **kwargs)
        response = serializers.serialize('json', func_response)
        # status_code = response.get('status_code', 200)
        return JsonResponse(response, safe=False)
    return func_wrapper
