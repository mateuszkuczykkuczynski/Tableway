from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from datetime import timedelta

from .serializers import TableSerializer, ReservationSerializerEditableFields, ReservationDetailsSerializer, \
    EmployeeSerializerEditableFields, EmployeeDetailsSerializer, AddEmployeeToReservationSerializer
from .models import Table, Reservation, Employee
from .permissions import IsOwnerOrAdmin


class AvailableTablesView(ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        queryset = Table.objects.all()
        restaurant_name = self.request.query_params.get('restaurant', None)
        restaurant_type = self.request.query_params.get('type', None)
        capacity = self.request.query_params.get('capacity', None)
        city = self.request.query_params.get('city', None)

        if restaurant_name:
            queryset = queryset.filter(location__name__icontains=restaurant_name)
        if restaurant_type:
            queryset = queryset.filter(location__restaurant_type=restaurant_type)
        if city:
            queryset = queryset.filter(location__city__name__icontains=city)
        if capacity:
            queryset = queryset.filter(capacity=capacity)

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
    lookup_field = 'pk'

# class AllRestaurantsAvailableTablesView(ListAPIView):
#     serializer_class = TableSerializer
#
#     def get_queryset(self):
#         capacity = self.kwargs['capacity']
#         restaurant_city = self.kwargs['city']
#         try:
#             table = Table.objects.filter(capacity=capacity, is_reserved=False)
#         except Table.DoesNotExist:
#             raise Http404
#         return table


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


class ReservationAddServiceView(UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = AddEmployeeToReservationSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def perform_update(self, serializer):
        if not self.request.user.is_superuser and self.request.user != serializer.instance.owner:
            raise PermissionDenied("You don't have permission to add service to this reservation.")

        serializer.save()
