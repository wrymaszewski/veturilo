from django.contrib import admin
from .models import Location, Snapshot, Stat

# Register your models here.
admin.site.register(Snapshot)
admin.site.register(Location)
admin.site.register(Stat)
