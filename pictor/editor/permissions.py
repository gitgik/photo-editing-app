from rest_framework import permissions


class IsAuthenticated(permissions.IsAuthenticated):
    """This class allows only authenticated users to access certain views."""

    def has_permissions(self, request, view):
        """Check whether user has permissions."""
        if request.method == 'POST':
            return True
        return super(
            IsAuthenticated, self).has_permissions(request, view)
