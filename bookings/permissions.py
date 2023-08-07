from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Restaurant

User = get_user_model()


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to allow only object owners and admins to modify it. All authenticated users can view.
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
        if obj.owner == request.user:
            return True
        return False


class IsOwnerOrAdminGET(permissions.BasePermission):
    """
    Permission to allow only object owners to view it when using safe methods (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):

        # Authenticated users only can see list view
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            if obj.owner == request.user:
                return True
        return False


class IsOwnerOrAdminPUT(permissions.BasePermission):
    """
    Permission to allow only object owners and associated service users to modify it. All can view using safe methods.
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
        if obj.owner == request.user or obj.service == request.user:
            return True
        return False


class IsOwnerOrAdminAddService(permissions.BasePermission):
    """
    Permission to allow only object owners and associated service users to modify it. All can view using safe methods.
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
        if obj.table_number.location.owner == request.user or obj.service == request.user:
            return True
        return False


class IsOwnerOrAdminGetList(permissions.BasePermission):
    """
    Permission to allow only restaurant owners to view the list of objects associated with their restaurant.
    """

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            if view.kwargs.get('restaurant_id'):
                restaurant_id = view.kwargs['restaurant_id']
                restaurant = get_object_or_404(Restaurant, id=restaurant_id)
                return restaurant.owner == request.user
            return False


class IsOwnerOrAdminUserReservations(permissions.BasePermission):
    """
    Permission to allow only reservation owners to view their reservations using safe methods.
    """

    def has_object_permission(self, request, view, obj):

        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS and obj.owner == request.user:
            return True
