from django.test import TestCase
from django.urls import reverse
from django.contrib.gis.geos import Point


from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from places_service.models import Place
from places_service.serializers import PlaceSerializer


class PlaceModelTest(TestCase):
    def setUp(self):
        self.place_data = {
            "name": "Test Place",
            "description": "Description of the test place",
            "geom": Point(0, 0, srid=4326),
        }

    def test_place_creation(self):
        place = Place.objects.create(**self.place_data)

        self.assertEqual(place.name, self.place_data["name"])
        self.assertEqual(place.description, self.place_data["description"])
        self.assertEqual(place.geom, self.place_data["geom"])

    def test_str_representation(self):
        place = Place.objects.create(**self.place_data)

        expected_str = f"Name: {self.place_data['name']}, Description: {self.place_data['description']}, Coordinates: {self.place_data['geom']}"
        self.assertEqual(str(place), expected_str)


class PlaceSerializerTest(TestCase):
    def test_serializer_data(self):
        place_data = {
            "id": 1,
            "name": "Test Place",
            "description": "A test place",
            "geom": Point(1, 2),
        }

        serializer = PlaceSerializer(data=place_data)
        serializer.is_valid()

        self.assertTrue(serializer.is_valid())

    def test_serializer_validation(self):
        invalid_place_data = {
            "id": 1,
            "name": "Test Place",
            "description": "A test place",
            "geom": "Invalid geometry",
        }

        serializer = PlaceSerializer(data=invalid_place_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("geom", serializer.errors)

    def test_serializer_save(self):
        valid_place_data = {
            "name": "Test Place",
            "description": "A test place",
            "geom": Point(1, 2),
        }

        serializer = PlaceSerializer(data=valid_place_data)
        serializer.is_valid()

        self.assertTrue(serializer.is_valid())

        saved_place = serializer.save()

        self.assertIsInstance(saved_place, Place)
        self.assertEqual(saved_place.name, "Test Place")
        self.assertEqual(saved_place.description, "A test place")


class PlaceViewSetTest(APITestCase):
    def setUp(self):
        self.url = reverse("places_service:place-list")
        self.client = APIClient()

        self.place1 = Place.objects.create(
            name="Place 1",
            description="Description 1",
            geom="SRID=4326;POINT(10 10)",
        )
        self.place2 = Place.objects.create(
            name="Place 2",
            description="Description 2",
            geom="SRID=4326;POINT(20 20)",
        )

    def test_list_places(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_place(self):
        url = reverse("places_service:place-list")
        data = {
            "name": "New Place",
            "description": "A new place",
            "geom": "SRID=4326;POINT(15 15)",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_place(self):
        url = reverse(
            "places_service:place-detail", kwargs={"pk": self.place1.pk}
        )
        response = self.client.get(url)
        serializer = PlaceSerializer(self.place1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_place(self):
        url = reverse(
            "places_service:place-detail", kwargs={"pk": self.place1.pk}
        )
        data = {
            "name": "Updated Place",
            "description": "An updated place",
            "geom": "SRID=4326;POINT(25 25)",
        }
        response = self.client.put(url, data)
        place = Place.objects.get(pk=self.place1.pk)
        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(place.name, "Updated Place")
        self.assertEqual(place.description, "An updated place")

    def test_partial_update_place(self):
        url = reverse(
            "places_service:place-detail", kwargs={"pk": self.place1.pk}
        )
        data = {"description": "An updated description"}
        response = self.client.patch(url, data)
        place = Place.objects.get(pk=self.place1.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(place.description, "An updated description")

    def test_delete_place(self):
        url = reverse(
            "places_service:place-detail", kwargs={"pk": self.place1.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Place.objects.filter(pk=self.place1.pk).exists())

    def test_closest_point(self):
        url = reverse("places_service:place-closest-point")
        params = {"latitude": 5, "longitude": 5}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination(self):
        for i in range(10):
            Place.objects.create(
                name=f"Place {i}",
                description=f"Description {i}",
                geom=Point(i, i),
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

        response = self.client.get(self.url + "?page=3&page_size=1001")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
