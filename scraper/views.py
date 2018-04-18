import numpy as np
import pandas as pd
import seaborn as sns
import plotly.offline as opy
import plotly.graph_objs as go


from django.shortcuts import render
from .models import Snapshot, Location, Stat
from django.views.generic import TemplateView
# Create your views here.


class SnapshotScatter(TemplateView):


    template_name = 'scraper/scatter.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = Snapshot.objects.filter(location__slug = self.kwargs.get('slug'))
        location_name = qs[0].location.name
        lst=[]
        for obj in qs:
            lst.append([
                obj.avail_bikes,
                obj.free_stands,
                obj.timestamp
            ])
        cols = ['avail_bikes', 'free_stands', 'timestamp']
        df = pd.DataFrame(lst, columns=cols)
        # df.timestamp.dt.round('1min')
        df['hour'] = df['timestamp'].dt.hour
        # scatterplot
        scatter_trace1 = go.Scatter(
            x = df['timestamp'],
            y = df['avail_bikes'],
            mode = 'lines+markers',
            name = 'Available Bicycles',
        )

        scatter_trace2 = go.Scatter(
            x = df['timestamp'],
            y = df['free_stands'],
            mode = 'lines+markers',
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

        # boxplot
        box_trace1 = go.Box(
        x = df['hour'],
        y = df['avail_bikes'],
        boxpoints = False,
        name = 'Available Bicycles',
        )
        box_trace2 = go.Box(
        x = df['hour'],
        y = df['free_stands'],
        boxpoints = False,
        name = 'Free Stands',
        )

        box_data = go.Data([box_trace1, box_trace2])
        box_layout = go.Layout(
            title = location_name,
            xaxis = {'title':'Time'},
            yaxis = {'title':'Number'},
            boxmode = 'group'
        )

        box_figure = go.Figure(
            data = box_data,
            layout = box_layout
        )
        box_div = opy.plot(
            box_figure,
            auto_open = False,
            output_type = 'div'
        )

        context['scatter'] = scatter_div
        context['box'] = box_div
        return context


class Avaraged(TemplateView):


    template_name = 'scraper/means.html'
