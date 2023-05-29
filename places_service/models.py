from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    geom = models.PointField(db_index=True)

    class Meta:
        db_table = "places"

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}, Coordinates: {self.geom}"
