from django.db import models
from location_field.models.plain import PlainLocationField

# Create your models here.

class Location(models.Model):

    name = models.CharField(max_length=255)
    all_stands = models.IntegerField()
    coordinates = PlainLocationField()

    def __str__(self):
        return self.name


class Snapshot(models.Model):


    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    avail_bikes = models.IntegerField()
    free_stands = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)


class Stat(models.Model):


    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    avail_bikes_mean = models.FloatField(null=True)
    free_stands_mean = models.FloatField(null=True)
    avail_bikes_sd = models.FloatField(null=True)
    free_stands_sd = models.FloatField(null=True)
    time = models.TimeField()
    month = models.DateField()
