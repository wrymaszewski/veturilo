from django.conf.urls import url
from . import views

app_name = 'scraper'

urlpatterns = [
    url(r'scatter/(?P<slug>[-\w]+)/$', views.Plots.as_view(), name='plots')
]
