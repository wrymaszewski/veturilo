import time
import pandas as pd
import datetime
import calendar
from pytz import timezone

import plotly.offline as opy
import plotly.graph_objs as go

from django.shortcuts import render
from .models import Snapshot, Location, Stat
from django.views.generic import TemplateView

# rest framework
from .serializers import LocationSerializer, SnapshotSerializer, StatSerializer
from rest_framework import generics


def get_months(location):
    """Getting months for statistics from a given Location object"""
    months = set()
    for stat in location.stats.all():
        if stat.month:
            months.add(stat.month)
    return sorted(list(months))

def correct_time(dtime):
    """
    Plotly only shows dates in UTC. It is a know issue. This function
    extracts the hourly difference between UTC and Warsaw time and corrects
    the datetime for plotting.
    """
    now = datetime.datetime.now(tz=timezone('Europe/Warsaw'))
    diff_str = str(now).split('+')[1]
    diff = int(diff_str.split(':')[0])
    delta = datetime.timedelta(hours = diff)
    if type(dtime) is datetime.time:
        # if time (stats)
        comb = datetime.datetime.combine(now, dtime) + delta
        return comb.time()
    else:
        # if datetime (snapshots)
        return dtime + delta

def draw_scatter(df, sd=False, weekend=None):
    """
    Draws scatterplots based on the args
    df -> Pandas DataFrame
    sd -> bool (optional)
    weekend -> bool (optional)
    """

    if weekend is None:
        dat = df
    elif weekend:
        dat = df[df['weekend']==True]
    else:
        dat = df[df['weekend']==False]

    if not sd:
        dat['free_stands_sd'] = dat['free_stands']
        dat['avail_bikes_sd'] = dat['avail_bikes']

    # available bikes
    trace1 = go.Scatter(
        x = dat['time'],
        y = dat['avail_bikes'],
        error_y = dict(
            type = 'data',
            array = dat['free_stands_sd'],
            visible=sd),
        mode = 'lines',
        name = 'Available Bikes',
    )

    # free stands
    trace2 = go.Scatter(
        x = dat['time'],
        y = dat['free_stands'],
        error_y = dict(
            type = 'data',
            array = dat['free_stands_sd'],
            visible=sd),
        mode = 'lines',
        name = 'Free Stands',
    )

    data = go.Data([trace1, trace2])

    layout = go.Layout(
        xaxis = {'title':'Time'},
        yaxis = {'title':'Number'},
        legend = dict(
            x=0,
            y=1,
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=12,
                color='#000'
            ),
            bgcolor='#E2E2E2',
            bordercolor='#FFFFFF',
            borderwidth=2
        )
    )

    figure = go.Figure(
        data = data,
        layout = layout
    )

    div = opy.plot(
        figure,
        auto_open = False,
        output_type = 'div',
        link_text='Export'
    )

    return div

class SnapshotPlots(TemplateView):


    template_name = 'scraper/plots.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        zone = timezone('Europe/Warsaw')
        #### plotting from snapshots ####
        snapshots = (Snapshot.objects
                        .filter(location__slug = self.kwargs.get('slug'))
                        .filter(timestamp__gte = datetime.datetime.now(tz=zone)
                                    -datetime.timedelta(hours=72))
                        .select_related()
                    )
        lst=[]
        for obj in snapshots:
            lst.append([
                obj.avail_bikes,
                obj.free_stands,
                obj.timestamp,
            ])
        cols = ['avail_bikes', 'free_stands', 'time']
        df = pd.DataFrame(lst, columns=cols)
        df['time'] = df['time'].apply(lambda x: correct_time(x))
        df.sort_values('time', inplace=True)

        locations = Location.objects.select_related()
        location = snapshots[0].location
        context['locations'] = locations
        context['months'] = get_months(location)
        context['location'] = location
        context['scatter'] = draw_scatter(df)
        return context


class StatPlots(TemplateView):

    template_name = 'scraper/stat.html'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        #### plotting from stats ####
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        #last day of the month is required here
        week, day = calendar.monthrange(year, month)
        stat = (Stat.objects
                    .filter(location__slug = self.kwargs.get('slug'))
                    .filter(month__exact = datetime.date(year, month, day))
                    .select_related()
                )
        lst=[]
        for obj in stat:
            lst.append([
                obj.avail_bikes_mean,
                obj.free_stands_mean,
                obj.avail_bikes_sd,
                obj.free_stands_sd,
                obj.time,
                obj.month,
                obj.weekend
            ])
        cols = [
            'avail_bikes',
            'free_stands',
            'avail_bikes_sd',
            'free_stands_sd',
            'time',
            'month',
            'weekend'
        ]
        df = pd.DataFrame(lst, columns=cols)
        df['time'] = df['time'].apply(lambda x: correct_time(x))
        df['time'] = df['time'].apply(lambda x: x.isoformat(timespec='minutes'))
        df.sort_values('time', inplace=True)

        location = stat[0].location
        context['months'] = get_months(location)
        context['locations'] = Location.objects.select_related()
        context['location'] = location
        context['stat_wd'] = draw_scatter(df, weekend=False, sd=True)
        context['stat_we'] = draw_scatter(df, weekend=True, sd=True)
        return context

# REST Framework views

class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationDetail(generics.RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class SnapshotList(generics.ListAPIView):
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer


class SnapshotDetail(generics.RetrieveAPIView):
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer


class StatList(generics.ListAPIView):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer

class StatDetail(generics.RetrieveAPIView):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
