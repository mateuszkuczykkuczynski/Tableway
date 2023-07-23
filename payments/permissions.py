from rest_framework import permissions, status
from django.http import HttpResponse


from bookings.models import Restaurant, Employee, Reservation
from .models import Payment

# TODO: Refactor of file is needed because there is a lot of repeated class and functionality that should be reduced


class IsSuperUser(permissions.BasePermission):
    """
    Base permission class to check if the user is a superuser.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsRestaurantEmployeeOrOwnerOrAdmin(IsSuperUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        if not request.user.is_authenticated:
            return False

        restaurant_id = view.kwargs.get('restaurant_id')

        is_owner = Restaurant.objects.filter(id=restaurant_id, owner=request.user).exists()
        is_employee = Employee.objects.filter(works_in_id=restaurant_id, id=request.user.id).exists()

        if is_owner or is_employee:
            return True
        return False


class IsOwnerOrAdminOfPayment(IsSuperUser):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        payment_id = view.kwargs.get('id')
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return False

        valid_ids = [
            payment.reservation.owner.id,
            payment.reservation.table_number.location.owner.id,
            payment.reservation.service.id,
        ]

        return request.user.id in valid_ids

    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            return True

        # Write permissions are only allowed to the account owner
        if obj.reservation.owner == request.user or obj.reservation.table_number.location.owner == request.user \
                or obj.reservation.service == request.user:
            return True
        return False


class IsOwnerOrAdminOfUserReservations(IsSuperUser):
    """
    Custom permission to only allow owners reservation to access data(including SAFE methods)
    """

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        user_id = view.kwargs['user_id']
        return request.user.id == user_id

    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            return True

        return request.user == obj.reservation.owner


class IsRestaurantOwnerOrAdmin(IsSuperUser):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        restaurant_id = view.kwargs['restaurant_id']

        try:
            return request.user.id == Restaurant.objects.get(id=restaurant_id).owner.id
        except Restaurant.DoesNotExist:
            return False


class CanPerformTipCreation(IsSuperUser):

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        if not request.user.is_authenticated:
            return False

        reservation_id = view.kwargs.get('reservation_id')
        is_reservation_owner = Reservation.objects.filter(id=reservation_id, owner=request.user).exists()

        if is_reservation_owner:
            return True

        return False

    # def has_object_permission(self, request, view, obj):
    #     return request.user == obj.owner


class IsTipsCreatorOrAdmin(IsSuperUser):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        # Check if the user_id in the URL matches the id of the currently authenticated user
        return view.kwargs['user_id'] == request.user.id

    # def has_permission(self, request, view):
    #     user_id = view.kwargs['user_id']
    #
    #     # return request.user == Tip.objects.get(reservation__owner=user_id).reservation.owner
    #     return request.user.id == user_id

    # def has_object_permission(self, request, view, obj):
    #     return obj.reservation.owner == request.user


class IsTipsOwnerOrAdmin(IsSuperUser):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        employee_id = view.kwargs['employee_id']
        try:
            is_owner = Restaurant.objects.filter(id=Employee.objects.get(id=employee_id).works_in.id,
                                                 owner=request.user.id).exists()
            # Check if the user_id in the URL matches the id of the currently authenticated user
            return view.kwargs['employee_id'] == request.user.id or is_owner
        except Employee.DoesNotExist:
            return False


class IsRestaurantOwnerWithTipsOrAdmin(IsSuperUser):
    """
    Custom permission to only allow owners of an object and admins to edit or delete it.
    """

    # def has_permission(self, request, view):
    #     user_id = view.kwargs['user_id']
    #
    #     # return request.user == Tip.objects.get(reservation__owner=user_id).reservation.owner
    #     return request.user.id == user_id

    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            return True

        return obj.reservation.table_number.location.owner == request.user
