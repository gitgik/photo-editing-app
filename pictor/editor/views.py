"""Define the pictor views."""
import os
import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View


class LoginRequiredMixin(object):
    """This mixin ensures that the user is authenticated before proceeding."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class LoginView(View):
    """This view defines the login view."""

    def get(self, request, *args, **kwargs):
        """Render the index/login view."""
        if request.user.is_authenticated():
            return redirect(reverse('pictor:dashboard'))

        context = {}
        context.update(csrf(self.request))
        return render(self.request, 'pictor/index.html', context)


class LogoutView(LoginRequiredMixin, View):
    """This View logs the authenticated user out."""

    def get(self, request, *args, **kwargs):
        """Flash user session and redirect them to login page."""
        logout(request)
        return redirect(reverse('pictor:index'))
