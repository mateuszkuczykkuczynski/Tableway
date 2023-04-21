from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.http import Http404

from .serializers import TableSerializer, ReservationSerializerEditableFields, ReservationDetailsSerializer
from .models import Table, Reservation


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
        table = get_object_or_404(Table, pk=request.data.get('table'))
        reserved = table.is_reserved_on_date(request.data.get('reserved_time'))
        if reserved:
            return Response({'error': 'Table is already reserved for the selected time'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            table.reservation = reservation
            table.is_reserved = True
            table.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelTableReservation(DestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.reserved_time = None
        instance.is_reserved = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
