import numpy as np
import pandas as pd
import seaborn as sns
import datetime
import calendar
import plotly.offline as opy
import plotly.graph_objs as go


from django.shortcuts import render
from .models import Snapshot, Location, Stat
from django.views.generic import TemplateView
# Create your views here.


class SnapshotPlots(TemplateView):


    template_name = 'scraper/plots.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        #### plotting from snapshots ####
        snapshots = (Snapshot.objects
                        .filter(location__slug = self.kwargs.get('slug'))
                        .filter(timestamp__gte = datetime.datetime.now()
                                    -datetime.timedelta(hours=24))
                        .select_related()
                    )
        location_name = snapshots[0].location.name
        lst=[]
        for obj in snapshots:
            lst.append([
                obj.avail_bikes,
                obj.free_stands,
                obj.timestamp,
                obj.weekend
            ])
        cols = ['avail_bikes', 'free_stands', 'timestamp', 'weekend']
        df = pd.DataFrame(lst, columns=cols)
        df['hour'] = df['timestamp'].dt.hour
        df.sort_values('timestamp', inplace=True)

        # scatterplot
        scatter_trace1 = go.Scatter(
            x = df['timestamp'],
            y = df['avail_bikes'],
            mode = 'lines',
            name = 'Available Bicycles',
        )

        scatter_trace2 = go.Scatter(
            x = df['timestamp'],
            y = df['free_stands'],
            mode = 'lines',
            name = 'Free Stands',
        )

        scatter_data = go.Data([scatter_trace1, scatter_trace2])
        scatter_layout = go.Layout(
            title = location_name,
            xaxis = {'title':'Time'},
            yaxis = {'title':'Number'}
        )
        scatter_figure = go.Figure(
            data = scatter_data,
            layout = scatter_layout
        )
        scatter_div = opy.plot(
            scatter_figure,
            auto_open = False,
            output_type = 'div'
        )

        locations = Location.objects.select_related()
        location = snapshots[0].location
        context['locations'] = locations

        months = set()
        for stat in location.stats.all():
            if stat.month:
                months.add(stat.month)
        months_list = list(months)
        context['months'] = sorted(months_list)
        context['location'] = location
        context['scatter'] = scatter_div
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
        location_name = stat[0].location.name

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
            'avail_bikes_mean',
            'free_stands_mean',
            'avail_bikes_sd',
            'free_stands_sd',
            'time',
            'month',
            'weekend'
        ]
        df = pd.DataFrame(lst, columns=cols)
        df.sort_values('time', inplace=True)


        # plots for weekdays
        trace1 = go.Scatter(
            x = df[df['weekend']==False]['time'],
            y = df[df['weekend']==False]['avail_bikes_mean'],
            error_y = dict(
                type = 'data',
                array = df['avail_bikes_sd'],
                visible=True
            ),
            mode = 'lines+markers',
            name = 'Available Bikes',
        )
        trace2 = go.Scatter(
            x = df[df['weekend']==False]['time'],
            y = df[df['weekend']==False]['free_stands_mean'],
            error_y = dict(
                type = 'data',
                array = df['free_stands_sd'],
                visible=True
            ),
            mode = 'lines+markers',
            name = 'Free Stands',
        )

        data = go.Data([trace1, trace2])

        layout = go.Layout(
            title = location_name,
            xaxis = {'title':'Time'},
            yaxis = {'title':'Number'}
        )
        figure = go.Figure(
            data = data,
            layout = layout
        )
        stat_wd_div = opy.plot(
            figure,
            auto_open = False,
            output_type = 'div'
        )

        # plots for weekends
        trace1 = go.Scatter(
            x = df[df['weekend']]['time'],
            y = df[df['weekend']]['avail_bikes_mean'],
            error_y = dict(
                type = 'data',
                array = df['avail_bikes_sd'],
                visible=True
            ),
            mode = 'lines+markers',
            name = 'Available Bikes',
        )
        trace2 = go.Scatter(
            x = df[df['weekend']]['time'],
            y = df[df['weekend']]['free_stands_mean'],
            error_y = dict(
                type = 'data',
                array = df['free_stands_sd'],
                visible=True
            ),
            mode = 'lines+markers',
            name = 'Free Stands',
        )

        data = go.Data([trace1, trace2])

        layout = go.Layout(
            title = location_name,
            xaxis = {'title':'Time'},
            yaxis = {'title':'Number'}
        )
        figure = go.Figure(
            data = data,
            layout = layout
        )
        stat_we_div = opy.plot(
            figure,
            auto_open = False,
            output_type = 'div'
        )

        context['locations'] = Location.objects.select_related()
        context['location'] = stat[0].location
        context['stat_wd'] = stat_wd_div
        context['stat_we'] = stat_we_div
        return context
