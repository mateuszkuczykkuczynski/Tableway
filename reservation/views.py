from rest_framework.generics import ListAPIView
from django.http import Http404

from .serializers import TableSerializer, RestaurantsSerializer
from .models import Table, Restaurant


class RestaurantAvailableTablesView(ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        restaurant_name = self.kwargs['restaurant']
        try:
            restaurant = Restaurant.objects.get(name=restaurant_name)
        except Restaurant.DoesNotExist:
            raise Http404
        return Table.objects.filter(location=restaurant)


class AllRestaurantsAvailableTablesView(ListAPIView):
    serializer_class = RestaurantsSerializer

    def get_queryset(self):
        restaurant_name = self.kwargs['restaurant']
        try:
            restaurant = Restaurant.objects.get(name=restaurant_name)
        except Restaurant.DoesNotExist:
            raise Http404
        return Table.objects.filter(location=restaurant)
