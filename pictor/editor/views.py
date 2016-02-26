"""Define the editor views."""
import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from decorators import json_response
from .enhancers import photo_effects
from pictor.settings import MAX_UPLOAD_SIZE


class LoginRequiredMixin(object):
    """This mixin ensures that the user is authenticated before proceeding."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Accept a request and return a response."""
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class JsonResponseMixin(object):
    """A mixin that returns a response in JSON format."""

    @method_decorator(json_response)
    def dispatch(self, request, *args, **kwargs):
        """Accept a request and return an override of dispatch."""
        return super(JsonResponseMixin, self).dispatch(
            request, *args, **kwargs)


class LoginView(View):
    """This view defines the login view."""

    def get(self, request, *args, **kwargs):
        """Render the index/login view."""
        if request.user.is_authenticated():
            return redirect(reverse('editor:dashboard'))

        context = {}
        context.update(csrf(self.request))
        return render(self.request, 'editor/index.html', context)


class DashboardView(View):
    """Represents the authenticated user dashboard."""

    def get(self, request, *args, **kwargs):
        """Render the dashboard view."""
        context = {
            'photo_effects': photo_effects,
        }
        context.update(csrf(self.request))
        return render(self.request, 'editor/index.html', context)


class LogoutView(LoginRequiredMixin, View):
    """This View logs the authenticated user out."""

    def get(self, request, *args, **kwargs):
        """Flash user session and redirect them to login page."""
        logout(request)
        return redirect(reverse('editor:index'))


class PhotoUploadView(LoginRequiredMixin, View):
    """View to handle image uploads from the authenticated user."""

    def post(self, request, *args, **kwargs):
        """Handle photo uploads."""
        pass
