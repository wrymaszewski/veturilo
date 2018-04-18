# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-18 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_auto_20180417_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='slug',
            field=models.CharField(default='slug', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='snapshot',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snapshots', to='scraper.Location'),
        ),
        migrations.AlterField(
            model_name='stat',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='scraper.Location'),
        ),
    ]