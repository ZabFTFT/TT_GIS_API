from django.core.exceptions import ValidationError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
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

    @extend_schema(
        description="Retrieve a list of places.",
        responses={200: PlaceSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Create a new place.",
        request=PlaceSerializer,
        responses={201: PlaceSerializer},
        examples=[
            OpenApiExample(
                name="Example 1 Create Place",
                value={
                    "name": "New Place",
                    "description": "A new place",
                    "geom": "SRID=4326;POINT(15 15)"
                },
                response_only=False
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Retrieve a single place by ID.",
        responses={200: PlaceSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Update a place by ID.",
        request=PlaceSerializer,
        responses={200: PlaceSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description="Partial update of a place by ID.",
        request=PlaceSerializer,
        responses={200: PlaceSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Delete a place by ID.",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="latitude",
                description="Latitude coordinate of the target location.",
                required=True,
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="longitude",
                description="Longitude coordinate of the target location.",
                required=True,
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
            ),
        ],
        description="Find the closest place to the given coordinates.",
        responses={200: PlaceSerializer()},
        examples=[
            OpenApiExample(
                name="Find Closest Place",
                value={
                    "latitude": 5,
                    "longitude": 5
                },
            )
        ],
    )
    @action(detail=False, methods=["get"])
    def closest_point(self, request):
        latitude_str = request.query_params.get("latitude")
        longitude_str = request.query_params.get("longitude")

        try:
            latitude = float(latitude_str)
            longitude = float(longitude_str)
        except ValueError:
            raise ValidationError("Invalid latitude or longitude values.")

        point = Point(longitude, latitude, srid=4326)

        closest_place = (
            Place.objects.annotate(distance=Distance("geom", point))
            .order_by("distance")
            .first()
        )

        serializer = self.get_serializer(closest_place)
        return Response(serializer.data)
