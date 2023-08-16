from datetime import timedelta
from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.shortcuts import Http404

from .models import Table, Reservation, Employee
from .serializers import (TableSerializer, ReservationSerializerEditableFields, ReservationDetailsSerializer,
                          EmployeeSerializerEditableFields, EmployeeDetailsSerializer,
                          AddEmployeeToReservationSerializer, EmployeesListSerializer, UserReservationsListSerializer,
                          RestaurantReservationsListSerializer, ReservationPaymentStatusSerializer)
from .permissions import (IsOwnerOrAdmin, IsOwnerOrAdminGET, IsOwnerOrAdminPUT, IsOwnerOrAdminAddService,
                          IsOwnerOrAdminGetList, IsOwnerOrAdminUserReservations)
from .tasks import send_feedback_email_table_booking_task


class AvailableTablesView(ListAPIView):
    """
    API view to list all available tables based on various filters such as restaurant name, type, capacity, and city.
    """
    serializer_class = TableSerializer

    def get_queryset(self):
        queryset = Table.objects.all()
        restaurant_name = self.request.query_params.get('restaurant', None)
        restaurant_type = self.request.query_params.get('type', None)
        capacity = self.request.query_params.get('capacity', None)
        city = self.request.query_params.get('city', None)

        if restaurant_name:
            queryset = queryset.filter(location__name=restaurant_name)
        if restaurant_type:
            queryset = queryset.filter(location__restaurant_type=restaurant_type)
        if city:
            queryset = queryset.filter(location__city__name=city)
        if capacity:
            queryset = queryset.filter(capacity=capacity)

        return queryset


class NowAvailableTablesView(ListAPIView):
    """
    API view to list tables that are currently available, filtered by capacity and city.
    """
    serializer_class = TableSerializer

    def get_queryset(self):
        queryset = Table.objects.all()
        capacity = self.request.query_params.get('capacity', None)
        city = self.request.query_params.get('city', None)
        current_time = timezone.now()

        if city:
            queryset = queryset.filter(location__city__name=city)
        if capacity:
            queryset = queryset.filter(capacity=capacity)

        queryset = queryset.exclude(reservation__reserved_time__lte=current_time,
                                    reservation__reserved_time_end__gt=current_time)

        return queryset


class TableDetailsView(RetrieveAPIView):
    """
    API view to retrieve details for a specific table.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableReservationView(CreateAPIView):
    """
    API view to allow users to reserve a specific table. It checks for table availability before confirming
    the reservation.
    """
    queryset = Table.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReservationSerializerEditableFields
        return TableSerializer

    def post(self, request, *args, **kwargs):
        table = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        time_end = serializer.validated_data['reserved_time'] + timedelta(
            minutes=serializer.validated_data['duration'],
        )
        table.is_reserved_on_date(serializer.validated_data['reserved_time'], time_end)
        if table.is_reserved is False:
            reservation = serializer.save()
            table.reservation.add(reservation)
            table.is_reserved = True
            table.save()
            send_feedback_email_table_booking_task.delay()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelTableReservationView(DestroyAPIView):
    """
    API view to allow users to cancel a specific table reservation.
    """
    queryset = Reservation.objects.all()
    permission_classes = (IsOwnerOrAdmin,)


class ReservationDetailsView(RetrieveAPIView):
    """
    API view to retrieve details for a specific reservation.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationDetailsSerializer
    permission_classes = (IsOwnerOrAdminGET,)
    lookup_field = 'pk'


class ReservationPaymentStatusView(UpdateAPIView):
    """
    API view to update the payment status of a specific reservation.
    """
    serializer_class = ReservationPaymentStatusSerializer
    queryset = Reservation.objects.all()
    permission_classes = (IsOwnerOrAdminPUT,)


class AllUserReservationsView(ListAPIView):
    """
    API view to list all reservations for a specific user. Raises a permission error if the requester is not the user
    or an admin.
    """
    serializer_class = UserReservationsListSerializer
    permission_classes = (IsOwnerOrAdminUserReservations,)  # Not needed, solved from in queryset (temporary solution)

    def get_queryset(self):
        owner = self.kwargs['pk']
        if owner == self.request.user.id:
            queryset = Reservation.objects.filter(owner_id=owner)
        else:
            raise PermissionDenied("You don't have permission to view this user's reservations.")

        if not queryset.exists():  # or get_object_or_404(queryset)
            raise Http404("No reservations found for this user.")
        return queryset


class AllRestaurantReservationsView(ListAPIView):
    """
    API view to list all reservations for a specific restaurant, with an optional filter for a specific date.
    """
    serializer_class = RestaurantReservationsListSerializer
    permission_classes = (IsOwnerOrAdminGetList,)

    def get_queryset(self):
        queryset = Reservation.objects.all()
        restaurant_id = self.kwargs['restaurant_id']
        date_param = self.request.query_params.get('date')

        if date_param:
            date = parse_date(date_param)
            if date:
                queryset = queryset.filter(table_number__location__id=restaurant_id, reserved_time__date=date)
        else:
            queryset = queryset.filter(table_number__location__id=restaurant_id)

        return queryset


class ReservationAddServiceView(UpdateAPIView):
    """
    API view to allow adding a service to a specific reservation.
    """
    queryset = Reservation.objects.all()
    serializer_class = AddEmployeeToReservationSerializer
    permission_classes = (IsOwnerOrAdminAddService,)


class EmployeeCreateView(CreateAPIView):
    """
    API view to create a new employee. It checks for permissions to ensure only the restaurant owner or a superuser
    can add an employee to a restaurant.
    """
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeSerializerEditableFields
        return EmployeeDetailsSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_superuser and self.request.user != serializer.validated_data['works_in'].owner:
            raise PermissionDenied("You don't have permission to add an employee to this restaurant.")


class EmployeeDetailsView(RetrieveAPIView):
    """
    API view to retrieve details for a specific employee.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailsSerializer
    lookup_field = 'pk'


class AllRestaurantEmployeesView(ListAPIView):
    """
    API view to list all employees for a specific restaurant.
    """
    serializer_class = EmployeesListSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()
        restaurant_name = self.request.query_params.get('restaurant', None)

        if restaurant_name:
            queryset = queryset.filter(works_in=restaurant_name)

        return queryset


class AllEmployeeReservationsView(ListAPIView):
    """
    API view to list all reservations served by a specific employee.
    """
    serializer_class = ReservationDetailsSerializer

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        queryset = Reservation.objects.filter(service__id=employee_id)
        return queryset
