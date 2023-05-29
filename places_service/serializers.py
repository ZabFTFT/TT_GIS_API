from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeometryField

from places_service.models import Place


class PlaceSerializer(ModelSerializer):
    geom = GeometryField()

    class Meta:
        model = Place
        fields = (
            "id",
            "name",
            "description",
            "geom",
        )
