"""Define the editor views."""
import os
import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from decorators import json_response
from forms import FacebookAuthForm


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


class FacebookAuthView(JsonResponseMixin, View):
    """Implement the facebook login Oauth."""

    def post(self, request, *args, **kwargs):
        """Log the user in and redirect them to the home page."""
        auth_form = FacebookAuthForm(request.POST)
        if auth_form.is_valid():
            user = auth_form.save()
            if user:
                profile = user.social_profile
                profile.extras = json.dumps(request.POST)
                profile.save()
                login(request, user)

                return {
                    'status': 'success',
                    'status_code': 200,
                    'loginRedirectURL': reverse('editor:dashboard'),
                }
        # return forbidden
        return {'status': 'Forbidden user', 'status_code': 403, }


class LoginView(View):
    """This view defines the login view."""

    def get(self, request, *args, **kwargs):
        """Render the index/login view."""
        if request.user.is_authenticated():
            return redirect(reverse('editor:dashboard'))

        context = {}
        context.update(csrf(self.request))
        return render(self.request, 'editor/index.html', context)


class DashboardView(JsonResponseMixin, View):
    """Represents the authenticated user dashboard."""

    def get(self, request, *args, **kwargs):
        """Render the dashboard view."""
        context = {
            'photo_effects': "Hey",
        }
        context.update(csrf(self.request))
        return render(self.request, 'editor/index.html', context)


class LogoutView(LoginRequiredMixin, View):
    """This View logs the authenticated user out."""

    def get(self, request, *args, **kwargs):
        """Flash user session and redirect them to login page."""
        logout(request)
        return redirect(reverse('editor:index'))
