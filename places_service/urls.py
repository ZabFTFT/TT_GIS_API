from django.urls import path, include
from rest_framework.routers import SimpleRouter

from places_service.views import PlaceViewSet

router = SimpleRouter()
router.register("places", PlaceViewSet, basename="place")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "places/closest_point/",
        PlaceViewSet.as_view({"get": "closest_point"}),
        name="place-closest-point",
    ),
]

app_name = "places_service"
