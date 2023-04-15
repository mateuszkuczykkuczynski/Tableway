from rest_framework.generics import ListAPIView
from django.http import Http404

from .serializers import TableSerializer
from .models import Table, Restaurant


class AvailableTablesView(ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        queryset = Table.objects.all()
        restaurant_name = self.request.query_params.get('restaurant', None)
        restaurant_type = self.request.query_params.get('type', None)
        capacity = self.request.query_params.get('capacity', None)
        city = self.request.query_params.get('city', None)

        # try:
        #     restaurant = Restaurant.objects.get(name=restaurant_name)
        #     r_type = Restaurant.objects.get(restaurant_type=restaurant_type)
        #     r_city = Restaurant.objects.get(city=city)
        # except Restaurant.DoesNotExist:
        #     raise Http404
        # return Table.objects.filter(location=restaurant and r_type and r_city, is_reserved=False, capacity=capacity)
        if restaurant_name:
            queryset = queryset.filter(location__name__icontains=restaurant_name)
        if restaurant_type:
            queryset = queryset.filter(location__restaurant_type=restaurant_type)
        if city:
            queryset = queryset.filter(location__city__name__icontains=city)
        if capacity:
            queryset = queryset.filter(capacity=capacity)

        return queryset

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
