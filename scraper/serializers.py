from rest_framework import serializers
from .models import Location, Snapshot, Stat

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('pk', 'name', 'all_stands', 'coordinates')


class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ('pk', 'location', 'avail_bikes', 'free_stands',
                 'timestamp', 'weekend')


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ('pk', 'location', 'avail_bikes_mean', 'free_stands_mean',
                'avail_bikes_sd', 'free_stands_sd', 'time', 'month', 'weekend')
