from rest_framework.serializers import ModelSerializer

from places_service.models import Place


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = (
            "id",
            "name",
            "description",
            "geom",
        )
