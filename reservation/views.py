from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from .serializers import TableSerializer, TableSerializerEditableFields
from .models import Table, Restaurant


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


class TableReservationView(UpdateAPIView):
    queryset = Table.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TableSerializerEditableFields
        return TableSerializer


class CancelTableReservation(DestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.reserved_time = None
        instance.is_reserved = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
