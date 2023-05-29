from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import action
from rest_framework.response import Response

from places_service.models import Place
from places_service.serializers import PlaceSerializer


class PlacePagination(PageNumberPagination):
    page_size = 5
    max_page_size = 1_000


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = PlacePagination

    @action(detail=False, methods=["get"])
    def closest_point(self, request):
        latitude = float(request.query_params.get("latitude"))
        longitude = float(request.query_params.get("longitude"))

        point = Point(longitude, latitude, srid=4326)

        closest_place = (
            Place.objects.annotate(distance=Distance("geom", point))
            .order_by("distance")
            .first()
        )

        serializer = self.get_serializer(closest_place)
        return Response(serializer.data)
