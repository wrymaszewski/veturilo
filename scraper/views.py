import numpy as np
import pandas as pd
import seaborn as sns
import plotly.offline as opy
import plotly.graph_objs as go


from django.shortcuts import render
from .models import Snapshot, Location, Stat
from django.views.generic import TemplateView
# Create your views here.


class Plots(TemplateView):


    template_name = 'scraper/plots.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)


        #### plotting from snapshots ####
        snapshots = (Snapshot.objects
                        .filter(location__slug = self.kwargs.get('slug'))
                        .select_related()
                    )
        location_name = snapshots[0].location.name
        lst=[]
        for obj in snapshots:
            lst.append([
                obj.avail_bikes,
                obj.free_stands,
                obj.timestamp
            ])
        cols = ['avail_bikes', 'free_stands', 'timestamp']
        df = pd.DataFrame(lst, columns=cols)
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

        #### plotting from stats ####

        stat = (Stat.objects
                    .filter(location__slug = self.kwargs.get('slug'))
                    .select_related()
                )

        stat_lst=[]
        for obj in stat:
            stat_lst.append([
                obj.avail_bikes_mean,
                obj.free_stands_mean,
                obj.avail_bikes_sd,
                obj.free_stands_sd,
                obj.time,
                obj.month,
            ])
        cols = [
            'avail_bikes_mean',
            'free_stands_mean',
            'avail_bikes_sd',
            'free_stands_sd',
            'time',
            'month',
        ]

        stat_df = pd.DataFrame(stat_lst, columns=cols)


        trace1 = go.Scatter(
            x = stat_df['time'],
            y = stat_df['avail_bikes_mean'],
            mode = 'lines+markers',
            name = 'Available Bikes',
        )
        trace2 = go.Scatter(
            x =  stat_df['time'],
            y = stat_df['free_stands_mean'],
            mode = 'lines+markers',
            name = 'Free Stands',
        )

        trace1_sd = go.Scatter(
            x = stat_df['time'],
            y = ((stat_df['avail_bikes_mean']-stat_df['avail_bikes_sd'])
                +(stat_df['avail_bikes_mean']+stat_df['avail_bikes_sd'])),
            fill='tozerox',
            line=go.Line(color='transparent'),
            showlegend=False,
            name = 'Available Bikes',
        )
        trace2_sd = go.Scatter(
            x = stat_df['time'],
            y = ((stat_df['free_stands_mean']-stat_df['free_stands_sd'])
                +(stat_df['free_stands_mean']+stat_df['free_stands_sd'])),
            fill='tozerox',
            line=go.Line(color='transparent'),
            showlegend=False,
            name = 'Free Stands',
        )

        scatter_data = go.Data([trace1, trace2, trace1_sd, trace2_sd])
        scatter_layout = go.Layout(
            title = location_name,
            xaxis = {'title':'Time'},
            yaxis = {'title':'Number'}
        )
        scatter_figure = go.Figure(
            data = scatter_data,
            layout = scatter_layout
        )
        stat_div = opy.plot(
            scatter_figure,
            auto_open = False,
            output_type = 'div'
        )


        context['stat'] = stat_div
        context['scatter'] = scatter_div
        context['box'] = box_div
        return context
