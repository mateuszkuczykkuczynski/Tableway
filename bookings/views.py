from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import timedelta


from .serializers import TableSerializer, ReservationSerializerEditableFields, ReservationDetailsSerializer, \
    EmployeeSerializerEditableFields, EmployeeDetailsSerializer, AddEmployeeToReservationSerializer,\
    EmployeesListSerializer, UserReservationsListSerializer, RestaurantReservationsListSerializer, \
    ReservationPaymentStatusSerializer
from .models import Table, Reservation, Employee
from .permissions import IsOwnerOrAdmin, IsOwnerOrAdminGET, IsOwnerOrAdminPUT, IsOwnerOrAdminAddService


class AvailableTablesView(ListAPIView):
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
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableReservationView(CreateAPIView):
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelTableReservationView(DestroyAPIView):
    queryset = Reservation.objects.all()
    permission_classes = (IsOwnerOrAdmin,)


class ReservationDetailsView(RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationDetailsSerializer
    permission_classes = (IsOwnerOrAdminGET,)
    lookup_field = 'pk'


# TODO: Test
class ReservationPaymentStatusView(UpdateAPIView):
    serializer_class = ReservationPaymentStatusSerializer
    queryset = Reservation.objects.all()
    permission_classes = (IsOwnerOrAdminPUT,)

    # def perform_update(self, serializer):
    #     if not self.request.user.is_superuser or \
    #            not self.request.user != serializer.instance.owner or \
    #             not self.request.user != serializer.instance.service:
    #         raise PermissionDenied("You don't have permission to add service to this reservation.")
    #
    #     serializer.save()


# TODO: Test
class AllUserReservationsView(ListAPIView):
    serializer_class = UserReservationsListSerializer

    def get_queryset(self):
        queryset = Reservation.objects.all()
        reservation_owner = self.request.query_params.get('owner', None)

        if reservation_owner:
            queryset = queryset.filter(owner=reservation_owner)

        return queryset


# TODO: Test.
class AllRestaurantReservationsView(ListAPIView):
    serializer_class = RestaurantReservationsListSerializer

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
    queryset = Reservation.objects.all()
    serializer_class = AddEmployeeToReservationSerializer
    permission_classes = (IsOwnerOrAdminAddService,)

    # def perform_update(self, serializer):
    #     if not self.request.user.is_superuser and self.request.user != serializer.instance.owner:
    #         raise PermissionDenied("You don't have permission to add service to this reservation.")
    #
    #     serializer.save()


class EmployeeCreateView(CreateAPIView):
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeSerializerEditableFields
        return EmployeeDetailsSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_superuser and self.request.user != serializer.validated_data['works_in'].owner:
            raise PermissionDenied("You don't have permission to add an employee to this restaurant.")


class EmployeeDetailsView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailsSerializer
    lookup_field = 'pk'


# TODO: test
class AllRestaurantEmployeesView(ListAPIView):
    serializer_class = EmployeesListSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()
        restaurant_name = self.request.query_params.get('restaurant', None)

        if restaurant_name:
            queryset = queryset.filter(works_in=restaurant_name)

        return queryset


class AllEmployeeReservationsView(ListAPIView):
    serializer_class = ReservationDetailsSerializer

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        queryset = Reservation.objects.filter(service__id=employee_id)
        return queryset
