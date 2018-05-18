from django.conf.urls import url
from . import views

app_name = 'scraper'

urlpatterns = [
    (url(r'^snapshot/(?P<slug>[-\w]+)/$',
    views.SnapshotPlots.as_view(), name='snapshot_plots')),
    (url(r'^stat/(?P<slug>[-\w]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
    views.StatPlots.as_view(), name='stat_plots')),
    # REST API
    (url(r'^api/location/(?P<pk>[0-9]+)/$',
    views.LocationDetail.as_view())),
    (url(r'^api/locations/$',
    views.LocationList.as_view())),
    (url(r'^api/snapshot/(?P<pk>[0-9]+)/$',
    views.SnapshotDetail.as_view())),
    (url(r'^api/snapshots/$',
    views.SnapshotList.as_view())),
    (url(r'^api/stat/(?P<slug>[-\w]+)/$',
    views.StatDetail.as_view())),
    (url(r'^api/stats/$',
    views.StatList.as_view()))
]
