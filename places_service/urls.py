from django.urls import path, include
from rest_framework.routers import SimpleRouter

from places_service.views import PlaceViewSet

router = SimpleRouter()
router.register("places", PlaceViewSet, basename="places")


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "places_service"
