from django.conf.urls import url
from . import views

app_name = 'scraper'

urlpatterns = [
    (url(r'snapshot/(?P<slug>[-\w]+)/$',
    views.SnapshotPlots.as_view(), name='snapshot_plots')),
    (url(r'stat/(?P<slug>[-\w]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
    views.StatPlots.as_view(), name='stat_plots')),
]
