from rest_framework import permissions, status
from django.http import HttpResponse


from bookings.models import Restaurant, Employee, Reservation
# from .models import Payment,

# TODO: Refactor of file is needed because there is a lot of repeated class and functionality that should be reduced


class CanPerformTipCreation(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        reservation_id = view.kwargs.get('reservation_id')

        is_reservation_owner = Reservation.objects.filter(id=reservation_id, owner=request.user).exists()
        if is_reservation_owner:
            return True

        return False

    # def has_object_permission(self, request, view, obj):
    #     return request.user == obj.owner


class IsReservationOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners reservation to access data(including SAFE methods)
    """

    def has_permission(self, request, view):
        user_id = view.kwargs['user_id']
        return request.user.id == user_id

    def has_object_permission(self, request, view, obj):
        return request.user == obj.reservation.owner


class IsReservationOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):

        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the account owner
        if obj.reservation.owner == request.user or obj.reservation.table_number.location.owner == request.user \
                or obj.reservation.service == request.user:
            return True
        return False


class IsRestaurantOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    def has_permission(self, request, view):
        restaurant_id = view.kwargs['restaurant_id']

        return request.user == Restaurant.objects.get(id=restaurant_id).owner


class IsTipsCreatorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    # def has_permission(self, request, view):
    #     user_id = view.kwargs['user_id']
    #
    #     # return request.user == Tip.objects.get(reservation__owner=user_id).reservation.owner
    #     return request.user.id == user_id

    def has_object_permission(self, request, view, obj):
        return obj.reservation.owner == request.user


class IsTipsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    # def has_permission(self, request, view):
    #     user_id = view.kwargs['user_id']
    #
    #     # return request.user == Tip.objects.get(reservation__owner=user_id).reservation.owner
    #     return request.user.id == user_id

    def has_object_permission(self, request, view, obj):
        return obj.reservation.owner == request.user


class IsRestaurantOwnerWithTipsOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    # def has_permission(self, request, view):
    #     user_id = view.kwargs['user_id']
    #
    #     # return request.user == Tip.objects.get(reservation__owner=user_id).reservation.owner
    #     return request.user.id == user_id

    def has_object_permission(self, request, view, obj):
        return obj.reservation.table_number.location.owner == request.user


# class IsRestaurantEmployeeOrOwnerPermission(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user.is_authenticated
#
#     def has_object_permission(self, request, view, obj):
#         return obj.reservation.location.owner == request.user or obj.reservation.table_number.service == request.user


class IsRestaurantEmployeeOrOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        restaurant_id = view.kwargs.get('restaurant_id')

        is_owner = Restaurant.objects.filter(id=restaurant_id, owner=request.user).exists()
        if is_owner:
            return True

        is_employee = Employee.objects.filter(works_in_id=restaurant_id, id=request.user.id).exists()
        if is_employee:
            return True

        return False
