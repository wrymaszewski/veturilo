from django.conf.urls import url
from . import views

app_name = 'scraper'

urlpatterns = [
    url(r'scatter/(?P<slug>[-\w]+)/$', views.SnapshotScatter.as_view(), name='scatter')
]
