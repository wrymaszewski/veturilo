import datetime

from django.db import models
from location_field.models.plain import PlainLocationField
from django.utils.text import slugify

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    all_stands = models.IntegerField()
    coordinates = PlainLocationField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Snapshot(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 related_name='snapshots')
    avail_bikes = models.IntegerField()
    free_stands = models.IntegerField()
    timestamp = models.DateTimeField()
    weekend = models.BooleanField()

    def save(self, *args, **kwargs):
        self.weekend = self.timestamp.weekday() in [5, 6]
        super().save(*args, **kwargs)


class Stat(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 related_name='stats')
    avail_bikes_mean = models.FloatField(null=True)
    free_stands_mean = models.FloatField(null=True)
    avail_bikes_sd = models.FloatField(null=True)
    free_stands_sd = models.FloatField(null=True)
    time = models.TimeField()
    month = models.DateField()
    weekend = models.BooleanField()
