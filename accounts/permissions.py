from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    IsOwnerOrAdmin is a custom permission class that restricts access to authenticated users and only allows owners of
    an object or admins to edit or delete it.

    The 'has_permission' method checks if the user is authenticated, allowing them to see the list view.

    The 'has_object_permission' method allows safe methods (GET, HEAD, OPTIONS) for all users.
    Write permissions (PUT, PATCH, DELETE) are only granted if the user is the owner of the object.
    """

    def has_permission(self, request, view):

        # Authenticated users only can see list view
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the account owner
        if obj.id == request.user.id:
            return True
        return False
