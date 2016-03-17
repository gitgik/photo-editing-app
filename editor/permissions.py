"""imports."""
from rest_framework import permissions


class Authenticate(permissions.IsAuthenticated):
    """This class allows only authenticated users to access certain views."""

    def has_permission(self, request, view):
        """Check whether user has permissions."""
        if request.method == 'POST':
            return True
        return super(
            Authenticate, self).has_permission(request, view)
